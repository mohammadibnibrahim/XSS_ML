import pytest
import numpy as np
import pandas as pd
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.utils.helpers import load_config, PROJECT_ROOT, LABEL_MAP
from src.models.classifiers import get_all_models, build_random_forest
from src.evaluation.evaluate import compute_metrics
@pytest.fixture
def config():
    return load_config()
@pytest.fixture
def sample_data():
    np.random.seed(42)
    n_samples = 200
    n_features = 66
    X = np.random.rand(n_samples, n_features)
    y = np.random.randint(0, 2, n_samples)
    return X, y
@pytest.fixture
def feature_names():
    return [
        "url_length", "url_number_special_characters", "url_special_characters", "url_tag_script",
        "url_tag_img", "url_attr_src", "url_event_onerror",
        "url_tag_script_embed", "url_cookie", "url_number_keywords_param",
        "url_number_dots", "url_number_ip",
        "html_tag_script", "html_tag_iframe", "html_tag_meta",
        "html_tag_object", "html_tag_embed", "html_tag_link",
        "html_tag_applet", "html_tag_frame", "html_tag_form",
        "html_tag_body", "html_tag_style", "html_tag_img",
        "html_tag_input", "html_tag_textarea", "html_attr_action",
        "html_attr_style", "html_attr_codebase", "html_attr_data",
        "html_attr_id", "html_attr_longdesc", "html_attr_src",
        "html_attr_value", "html_attr_http-equiv", "html_event_onblur",
        "html_event_onchange", "html_event_onclick", "html_event_onerror",
        "html_event_onfocus", "html_event_onkeydown", "html_event_onkeypress",
        "html_event_onkeyup", "html_event_onload", "html_event_onmousedown",
        "html_event_onmousemove", "html_event_onmouseup", "html_event_onresize",
        "html_event_onselect", "html_number_keywords_evil",
        "js_pseudo_protocol", "js_dom_location",
        "js_prop_cookie", "js_prop_referrer",
        "js_method_write", "js_method_getElementsByTagName",
        "js_method_alert", "js_method_eval",
        "js_method_setTimeout", "js_method_confirm",
        "js_method_prompt", "js_min_function_calls",
        "js_length", "html_length",
    ]
class TestConfiguration:
    def test_config_loads_successfully(self, config):
        assert config is not None
        assert isinstance(config, dict)
    def test_config_has_required_sections(self, config):
        required_keys = ["data", "models", "training", "output"]
        for key in required_keys:
            assert key in config, f"Missing config section: {key}"
    def test_config_data_section(self, config):
        data = config["data"]
        assert "raw_url" in data
        assert "target_column" in data
        assert data["target_column"] == "class"
        assert 0 < data["test_size"] < 1
        assert 0 < data["val_size"] < 1
    def test_config_model_params(self, config):
        models = config["models"]
        assert "random_forest" in models
        assert "xgboost" in models
        assert "logistic_regression" in models
class TestModels:
    def test_all_models_build(self, config):
        models = get_all_models(config)
        assert len(models) == 3
        assert "Random Forest" in models
        assert "XGBoost" in models
        assert "Logistic Regression" in models
    def test_random_forest_fits_and_predicts(self, config, sample_data):
        X, y = sample_data
        model = build_random_forest(config)
        model.fit(X, y)
        predictions = model.predict(X)
        assert len(predictions) == len(y)
        assert set(predictions).issubset({0, 1})
    def test_model_predict_proba(self, config, sample_data):
        X, y = sample_data
        model = build_random_forest(config)
        model.fit(X, y)
        proba = model.predict_proba(X)
        assert proba.shape == (len(X), 2)
        assert np.allclose(proba.sum(axis=1), 1.0)
class TestEvaluation:
    def test_compute_metrics_basic(self):
        y_true = np.array([0, 0, 1, 1, 1, 0, 1, 0])
        y_pred = np.array([0, 0, 1, 1, 0, 0, 1, 1])
        metrics = compute_metrics(y_true, y_pred)
        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1_score" in metrics
        assert 0 <= metrics["accuracy"] <= 1
        assert 0 <= metrics["f1_score"] <= 1
    def test_compute_metrics_with_proba(self):
        y_true = np.array([0, 0, 1, 1, 1, 0, 1, 0])
        y_pred = np.array([0, 0, 1, 1, 0, 0, 1, 1])
        y_prob = np.array([0.1, 0.2, 0.9, 0.8, 0.4, 0.3, 0.85, 0.6])
        metrics = compute_metrics(y_true, y_pred, y_prob)
        assert "roc_auc" in metrics
        assert "avg_precision" in metrics
        assert 0 <= metrics["roc_auc"] <= 1
    def test_perfect_predictions(self):
        y = np.array([0, 0, 1, 1, 0, 1])
        metrics = compute_metrics(y, y)
        assert metrics["accuracy"] == 1.0
        assert metrics["f1_score"] == 1.0
class TestDataIntegrity:
    def test_feature_names_count(self, feature_names):
        assert len(feature_names) == 66
    def test_label_map_complete(self):
        assert 0 in LABEL_MAP
        assert 1 in LABEL_MAP
    def test_no_duplicate_feature_names(self, feature_names):
        assert len(feature_names) == len(set(feature_names))
class TestPreprocessing:
    def test_split_proportions(self, sample_data, config):
        from src.preprocessing.preprocess import preprocess_and_split
        X, y = sample_data
        feature_names = [f"feature_{i}" for i in range(66)]
        df = pd.DataFrame(X, columns=feature_names)
        df["class"] = y
        data = preprocess_and_split(df, config)
        total = len(data["X_train"]) + len(data["X_val"]) + len(data["X_test"])
        assert total <= len(X)
        test_ratio = len(data["X_test"]) / total
        assert 0.10 <= test_ratio <= 0.20
    def test_scaling_applied(self, sample_data, config):
        from src.preprocessing.preprocess import preprocess_and_split
        X, y = sample_data
        feature_names = [f"feature_{i}" for i in range(66)]
        df = pd.DataFrame(X, columns=feature_names)
        df["class"] = y
        data = preprocess_and_split(df, config)
        means = np.abs(data["X_train"].mean(axis=0))
        assert np.all(means < 0.5), "Training data means should be near zero"
