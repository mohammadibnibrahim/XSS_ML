from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from src.utils.helpers import setup_logging
logger = setup_logging()
def build_random_forest(config):
    params = config["models"]["random_forest"]
    model = RandomForestClassifier(**params)
    logger.info(f"Built RandomForest: n_estimators={params['n_estimators']}, "
                f"max_depth={params['max_depth']}")
    return model
def build_xgboost(config):
    params = config["models"]["xgboost"]
    model = XGBClassifier(**params)
    logger.info(f"Built XGBoost: n_estimators={params['n_estimators']}, "
                f"max_depth={params['max_depth']}, lr={params['learning_rate']}")
    return model
def build_logistic_regression(config):
    params = config["models"]["logistic_regression"]
    model = LogisticRegression(**params)
    logger.info(f"Built LogisticRegression: C={params['C']}, solver={params['solver']}")
    return model
def get_all_models(config):
    return {
        "Random Forest": build_random_forest(config),
        "XGBoost": build_xgboost(config),
        "Logistic Regression": build_logistic_regression(config),
    }
