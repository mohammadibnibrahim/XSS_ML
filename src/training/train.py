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
    logger.info(f"Training {model_name} ...")
    start = time.time()
    model.fit(X_train, y_train)
    elapsed = time.time() - start
    logger.info(f"{model_name} trained in {elapsed:.2f}s")
    return model
def cross_validate_model(model, X_train, y_train, config, model_name="model"):
    n_folds = config["training"]["cv_folds"]
    rs = config["training"]["random_state"]
    scoring = ["accuracy", "precision", "recall", "f1"]
    logger.info(f"Running {n_folds}-fold CV for {model_name} ...")
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
    for metric in scoring:
        key = f"test_{metric}"
        mean = cv_results[key].mean()
        std = cv_results[key].std()
        logger.info(f"  {metric}: {mean:.4f} ± {std:.4f}")
    return cv_results
def save_model(model, model_name, config):
    models_dir = PROJECT_ROOT / config["output"]["models_dir"]
    ensure_dir(models_dir)
    safe_name = model_name.lower().replace(" ", "_")
    filepath = models_dir / f"{safe_name}.joblib"
    joblib.dump(model, filepath)
    logger.info(f"Saved {model_name} -> {filepath}")
    return filepath
def train_all_models(data, config):
    models = get_all_models(config)
    results = {}
    X_train = data["X_train"]
    y_train = data["y_train"]
    for name, model in models.items():
        cv_results = cross_validate_model(model, X_train, y_train, config, name)
        trained = train_model(model, X_train, y_train, name)
        save_model(trained, name, config)
        results[name] = {
            : trained,
            : cv_results,
        }
    return results
if __name__ == "__main__":
    from src.preprocessing.preprocess import load_processed_data
    config = load_config()
    data = load_processed_data(config)
    results = train_all_models(data, config)
    logger.info("Training pipeline completed successfully.")
