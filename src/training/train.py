"""
train.py — Model training pipeline with cross-validation.

Trains all configured classifiers, performs stratified k-fold
cross-validation, and persists the fitted models to disk.

Authors: Mohammad Ibrahim, Omar Adel, Mohamed Ahmed
Team: Blackhat — University of East London
Module: Level 4 Primers (Dr. Wael El Sersy)
"""

import time
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import StratifiedKFold, cross_validate

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.utils.helpers import load_config, setup_logging, ensure_dir, PROJECT_ROOT
from src.models.classifiers import get_all_models

logger = setup_logging()


def train_model(model, X_train, y_train, model_name="model"):
    """
    Fit a single model on the training data and report elapsed time.

    Parameters
    ----------
    model : sklearn-compatible estimator
        Un-fitted classifier.
    X_train : np.ndarray
        Training feature matrix.
    y_train : np.ndarray
        Training labels.
    model_name : str
        Human-readable model name for logging.

    Returns
    -------
    estimator
        The fitted model.
    """
    logger.info(f"Training {model_name} …")
    start = time.time()
    model.fit(X_train, y_train)
    elapsed = time.time() - start
    logger.info(f"{model_name} trained in {elapsed:.2f}s")
    return model


def cross_validate_model(model, X_train, y_train, config, model_name="model"):
    """
    Run stratified k-fold cross-validation and return per-fold metrics.

    Parameters
    ----------
    model : sklearn-compatible estimator
        Un-fitted classifier (will be cloned internally by sklearn).
    X_train : np.ndarray
        Training feature matrix.
    y_train : np.ndarray
        Training labels.
    config : dict
        Project configuration.
    model_name : str
        Human-readable model name for logging.

    Returns
    -------
    dict
        Cross-validation results with keys like 'test_accuracy',
        'test_precision', 'test_recall', 'test_f1'.
    """
    n_folds = config["training"]["cv_folds"]
    rs = config["training"]["random_state"]

    scoring = ["accuracy", "precision", "recall", "f1"]

    logger.info(f"Running {n_folds}-fold CV for {model_name} …")
    start = time.time()

    cv = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=rs)
    cv_results = cross_validate(
        model, X_train, y_train,
        cv=cv,
        scoring=scoring,
        return_train_score=False,
        n_jobs=-1,
    )

    elapsed = time.time() - start
    logger.info(f"{model_name} CV completed in {elapsed:.2f}s")

    # Log summary
    for metric in scoring:
        key = f"test_{metric}"
        mean = cv_results[key].mean()
        std = cv_results[key].std()
        logger.info(f"  {metric}: {mean:.4f} ± {std:.4f}")

    return cv_results


def save_model(model, model_name, config):
    """
    Persist a trained model to disk as a joblib file.

    Parameters
    ----------
    model : fitted estimator
        Trained classifier.
    model_name : str
        Human-readable name (used to build filename).
    config : dict
        Project configuration.

    Returns
    -------
    Path
        Path to the saved model file.
    """
    models_dir = PROJECT_ROOT / config["output"]["models_dir"]
    ensure_dir(models_dir)

    # Create a filesystem-safe filename
    safe_name = model_name.lower().replace(" ", "_")
    filepath = models_dir / f"{safe_name}.joblib"

    joblib.dump(model, filepath)
    logger.info(f"Saved {model_name} → {filepath}")

    return filepath


def train_all_models(data, config):
    """
    Train all models, run cross-validation, and save to disk.

    Parameters
    ----------
    data : dict
        Preprocessed data (from preprocess.py).
    config : dict
        Project configuration.

    Returns
    -------
    dict
        Mapping of model_name → {'model': fitted_model, 'cv_results': dict}.
    """
    models = get_all_models(config)
    results = {}

    X_train = data["X_train"]
    y_train = data["y_train"]

    for name, model in models.items():
        # Cross-validation (uses cloned copies internally)
        cv_results = cross_validate_model(model, X_train, y_train, config, name)

        # Train on full training set
        trained = train_model(model, X_train, y_train, name)

        # Save to disk
        save_model(trained, name, config)

        results[name] = {
            "model": trained,
            "cv_results": cv_results,
        }

    return results


# ── Standalone execution ───────────────────────────────────────────────
if __name__ == "__main__":
    from src.preprocessing.preprocess import load_processed_data

    config = load_config()
    data = load_processed_data(config)
    results = train_all_models(data, config)
    logger.info("Training pipeline completed successfully.")
