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
    df = pd.DataFrame(X, columns=feature_names)
    corr = df.corr()
    logger.info(f"Computed correlation matrix ({corr.shape[0]}×{corr.shape[1]})")
    return corr
def get_feature_importance(model, feature_names):
    importances = model.feature_importances_
    df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances,
    }).sort_values("importance", ascending=False).reset_index(drop=True)
    logger.info(f"Top-5 features: {df.head(5)['feature'].tolist()}")
    return df
def analyse_feature_groups(importance_df):
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
