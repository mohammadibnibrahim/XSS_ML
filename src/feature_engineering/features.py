"""
features.py — Feature analysis and importance visualisation.

Analyses feature correlations, generates importance rankings from
trained tree-based models, and compares feature-group contributions
(URL vs HTML vs JavaScript features).

Authors: Mohammad Ibrahim, Omar Adel, Mohamed Ahmed
Team: Blackhat — University of East London
Module: Level 4 Primers (Dr. Wael El Sersy)
"""

import numpy as np
import pandas as pd
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.utils.helpers import (
    load_config, setup_logging, PROJECT_ROOT,
    URL_FEATURES, HTML_FEATURES, JS_FEATURES,
)

logger = setup_logging()


def compute_correlation_matrix(X, feature_names):
    """
    Compute the Pearson correlation matrix for all features.

    Parameters
    ----------
    X : np.ndarray
        Feature matrix (any split — typically training).
    feature_names : list of str
        Corresponding feature names.

    Returns
    -------
    pd.DataFrame
        Correlation matrix with features as both index and columns.
    """
    df = pd.DataFrame(X, columns=feature_names)
    corr = df.corr()
    logger.info(f"Computed correlation matrix ({corr.shape[0]}×{corr.shape[1]})")
    return corr


def get_feature_importance(model, feature_names):
    """
    Extract feature importances from a tree-based model.

    Parameters
    ----------
    model : fitted sklearn/xgboost estimator
        Must expose a .feature_importances_ attribute.
    feature_names : list of str
        Feature names matching the training data columns.

    Returns
    -------
    pd.DataFrame
        Sorted DataFrame with columns ['feature', 'importance'].
    """
    importances = model.feature_importances_
    df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances,
    }).sort_values("importance", ascending=False).reset_index(drop=True)

    logger.info(f"Top-5 features: {df.head(5)['feature'].tolist()}")
    return df


def analyse_feature_groups(importance_df):
    """
    Aggregate feature importances by category group
    (URL / HTML / JavaScript).

    Parameters
    ----------
    importance_df : pd.DataFrame
        Output from get_feature_importance().

    Returns
    -------
    pd.DataFrame
        Aggregated importances with columns ['group', 'total_importance'].
    """
    def classify_feature(name):
        if name in URL_FEATURES:
            return "URL Features"
        elif name in HTML_FEATURES:
            return "HTML Features"
        elif name in JS_FEATURES:
            return "JavaScript Features"
        else:
            return "Other"

    importance_df = importance_df.copy()
    importance_df["group"] = importance_df["feature"].apply(classify_feature)

    group_summary = (
        importance_df
        .groupby("group")["importance"]
        .sum()
        .reset_index()
        .rename(columns={"importance": "total_importance"})
        .sort_values("total_importance", ascending=False)
    )

    logger.info(f"Feature group importances:\n{group_summary}")
    return group_summary
