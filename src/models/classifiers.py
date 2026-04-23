"""
classifiers.py — Model definitions for XSS detection.

Provides factory functions that build configured scikit-learn and
XGBoost classifiers from the project configuration file.

Authors: Mohammad Ibrahim, Omar Adel, Mohamed Ahmed
Team: Blackhat — University of East London
Module: Level 4 Primers (Dr. Wael El Sersy)
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.utils.helpers import setup_logging

logger = setup_logging()


def build_random_forest(config):
    """
    Construct a Random Forest classifier from config parameters.

    Parameters
    ----------
    config : dict
        Project configuration (expects config['models']['random_forest']).

    Returns
    -------
    RandomForestClassifier
        Un-fitted classifier.
    """
    params = config["models"]["random_forest"]
    model = RandomForestClassifier(**params)
    logger.info(f"Built RandomForest: n_estimators={params['n_estimators']}, "
                f"max_depth={params['max_depth']}")
    return model


def build_xgboost(config):
    """
    Construct an XGBoost classifier from config parameters.

    Parameters
    ----------
    config : dict
        Project configuration (expects config['models']['xgboost']).

    Returns
    -------
    XGBClassifier
        Un-fitted classifier.
    """
    params = config["models"]["xgboost"]
    model = XGBClassifier(**params)
    logger.info(f"Built XGBoost: n_estimators={params['n_estimators']}, "
                f"max_depth={params['max_depth']}, lr={params['learning_rate']}")
    return model


def build_logistic_regression(config):
    """
    Construct a Logistic Regression classifier from config parameters.

    Parameters
    ----------
    config : dict
        Project configuration (expects config['models']['logistic_regression']).

    Returns
    -------
    LogisticRegression
        Un-fitted classifier.
    """
    params = config["models"]["logistic_regression"]
    model = LogisticRegression(**params)
    logger.info(f"Built LogisticRegression: C={params['C']}, solver={params['solver']}")
    return model


def get_all_models(config):
    """
    Build and return all three classifiers as a dictionary.

    Parameters
    ----------
    config : dict
        Project configuration.

    Returns
    -------
    dict
        Mapping of model name (str) → un-fitted estimator.
    """
    return {
        "Random Forest": build_random_forest(config),
        "XGBoost": build_xgboost(config),
        "Logistic Regression": build_logistic_regression(config),
    }
