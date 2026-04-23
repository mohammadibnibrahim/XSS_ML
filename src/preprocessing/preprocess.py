"""
preprocess.py — Data loading, cleaning, and splitting pipeline.

Downloads the XSS dataset from GitHub (if not cached locally),
performs exploratory sanity checks, applies stratified train/val/test
splitting, and scales features using StandardScaler.  All artefacts
are persisted to data/processed/ for reproducibility.

Authors: Mohammad Ibrahim, Omar Adel, Mohamed Ahmed
Team: Blackhat — University of East London
Module: Level 4 Primers (Dr. Wael El Sersy)
"""

import os
import urllib.request
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Allow running as a standalone script or as an imported module
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.utils.helpers import load_config, setup_logging, ensure_dir, PROJECT_ROOT


logger = setup_logging()


def download_dataset(config):
    """
    Download the raw CSV dataset from GitHub if it is not already
    present in the local data/raw/ directory.

    Parameters
    ----------
    config : dict
        Project configuration dictionary.

    Returns
    -------
    Path
        Absolute path to the downloaded (or already existing) CSV file.
    """
    raw_dir = PROJECT_ROOT / config["data"]["raw_dir"]
    ensure_dir(raw_dir)

    filepath = raw_dir / config["data"]["raw_filename"]

    if filepath.exists():
        logger.info(f"Dataset already exists at {filepath}")
        return filepath

    url = config["data"]["raw_url"]
    logger.info(f"Downloading dataset from {url} ...")

    urllib.request.urlretrieve(url, filepath)
    logger.info(f"Dataset saved to {filepath}  ({filepath.stat().st_size / 1e6:.1f} MB)")

    return filepath


def load_dataset(filepath):
    """
    Load the CSV dataset into a pandas DataFrame.

    The CSV from the repository already contains a header row.
    The target column is named 'Label' in the original file;
    we rename it to 'class' for consistency across the pipeline.

    Parameters
    ----------
    filepath : str or Path
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded dataset with named columns.
    """
    df = pd.read_csv(filepath, low_memory=False)
    logger.info(f"Loaded CSV with {df.shape[1]} columns and {len(df)} rows")

    # Normalise the target column name
    # The original CSV uses 'Label'; our pipeline expects 'class'
    if "Label" in df.columns and "class" not in df.columns:
        df = df.rename(columns={"Label": "class"})
        logger.info("Renamed target column 'Label' -> 'class'")

    # Ensure all columns are numeric
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def explore_dataset(df):
    """
    Print basic exploratory statistics about the dataset.

    Parameters
    ----------
    df : pd.DataFrame
        The loaded dataset.

    Returns
    -------
    dict
        Summary statistics dictionary for downstream use.
    """
    stats = {}

    logger.info(f"Dataset shape: {df.shape}")
    stats["shape"] = df.shape

    logger.info(f"Missing values per column (total): {df.isnull().sum().sum()}")
    stats["total_missing"] = int(df.isnull().sum().sum())

    logger.info(f"Duplicate rows: {df.duplicated().sum()}")
    stats["duplicates"] = int(df.duplicated().sum())

    target_col = "class" if "class" in df.columns else "Label"
    class_dist = df[target_col].value_counts()
    logger.info(f"Class distribution:\n{class_dist}")
    stats["class_distribution"] = class_dist.to_dict()

    imbalance_ratio = class_dist.min() / class_dist.max()
    logger.info(f"Imbalance ratio (minority/majority): {imbalance_ratio:.3f}")
    stats["imbalance_ratio"] = float(imbalance_ratio)

    return stats


def preprocess_and_split(df, config):
    """
    Clean the dataset, split into train/validation/test sets, and
    apply StandardScaler normalisation.

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataset.
    config : dict
        Project configuration.

    Returns
    -------
    dict
        Dictionary containing X_train, X_val, X_test, y_train, y_val,
        y_test (all as NumPy arrays), feature_names, and the fitted scaler.
    """
    # ── 1. Drop duplicates ──────────────────────────────────────────
    initial_len = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    logger.info(f"Dropped {initial_len - len(df)} duplicate rows")

    # ── 2. Handle missing values (fill with median) ─────────────────
    if df.isnull().sum().sum() > 0:
        df = df.fillna(df.median())
        logger.info("Filled missing values with column medians")

    # ── 3. Separate features and target ─────────────────────────────
    target_col = config["data"]["target_column"]
    feature_cols = [c for c in df.columns if c != target_col]

    X = df[feature_cols].values
    y = df[target_col].values.astype(int)

    # ── 4. Stratified train / val / test split ──────────────────────
    test_size = config["data"]["test_size"]
    val_size = config["data"]["val_size"]
    rs = config["data"]["random_state"]

    # First split: separate test set
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=rs, stratify=y
    )

    # Second split: separate validation from training
    relative_val = val_size / (1 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=relative_val, random_state=rs, stratify=y_temp
    )

    logger.info(
        f"Split sizes — Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}"
    )

    # ── 5. Feature scaling ──────────────────────────────────────────
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    X_test = scaler.transform(X_test)

    logger.info("Applied StandardScaler normalisation")

    return {
        "X_train": X_train,
        "X_val": X_val,
        "X_test": X_test,
        "y_train": y_train,
        "y_val": y_val,
        "y_test": y_test,
        "feature_names": feature_cols,
        "scaler": scaler,
    }


def save_processed_data(data, config):
    """
    Persist processed data splits and the scaler to disk.

    Parameters
    ----------
    data : dict
        Output from preprocess_and_split().
    config : dict
        Project configuration.
    """
    out_dir = PROJECT_ROOT / config["data"]["processed_dir"]
    ensure_dir(out_dir)

    # Save numpy arrays
    np.save(out_dir / "X_train.npy", data["X_train"])
    np.save(out_dir / "X_val.npy", data["X_val"])
    np.save(out_dir / "X_test.npy", data["X_test"])
    np.save(out_dir / "y_train.npy", data["y_train"])
    np.save(out_dir / "y_val.npy", data["y_val"])
    np.save(out_dir / "y_test.npy", data["y_test"])

    # Save feature names
    pd.Series(data["feature_names"]).to_csv(
        out_dir / "feature_names.csv", index=False, header=False
    )

    # Save the fitted scaler
    joblib.dump(data["scaler"], out_dir / "scaler.joblib")

    logger.info(f"Processed data saved to {out_dir}")


def load_processed_data(config):
    """
    Load previously saved processed data from disk.

    Parameters
    ----------
    config : dict
        Project configuration.

    Returns
    -------
    dict
        Same structure as preprocess_and_split() output.
    """
    d = PROJECT_ROOT / config["data"]["processed_dir"]

    return {
        "X_train": np.load(d / "X_train.npy"),
        "X_val": np.load(d / "X_val.npy"),
        "X_test": np.load(d / "X_test.npy"),
        "y_train": np.load(d / "y_train.npy"),
        "y_val": np.load(d / "y_val.npy"),
        "y_test": np.load(d / "y_test.npy"),
        "feature_names": pd.read_csv(
            d / "feature_names.csv", header=None
        )[0].tolist(),
        "scaler": joblib.load(d / "scaler.joblib"),
    }


# ── Standalone execution ───────────────────────────────────────────────
if __name__ == "__main__":
    config = load_config()
    filepath = download_dataset(config)
    df = load_dataset(filepath)
    stats = explore_dataset(df)
    data = preprocess_and_split(df, config)
    save_processed_data(data, config)
    logger.info("Preprocessing pipeline completed successfully.")
