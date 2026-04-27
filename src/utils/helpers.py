import os
import yaml
import logging
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
URL_FEATURES = [
    , "url_special_characters", "url_tag_script",
    , "url_attr_src", "url_event_onerror",
    , "url_cookie", "url_number_keywords_param",
    , "url_number_ip",
]
HTML_FEATURES = [
    , "html_tag_iframe", "html_tag_meta",
    , "html_tag_embed", "html_tag_link",
    , "html_tag_frame", "html_tag_form",
    , "html_tag_style", "html_tag_img",
    , "html_tag_textarea", "html_attr_action",
    , "html_attr_codebase", "html_attr_data",
    , "html_attr_longdesc", "html_attr_src",
    , "html_attr_http-equiv", "html_event_onblur",
    , "html_event_onclick", "html_event_onerror",
    , "html_event_onkeydown", "html_event_onkeypress",
    , "html_event_onload", "html_event_onmousedown",
    , "html_event_onmouseup", "html_event_onresize",
    , "html_number_keywords_evil",
]
JS_FEATURES = [
    , "js_pseudo_protocol", "js_dom_location",
    , "js_prop_cookie", "js_prop_referrer",
    , "js_method_getElementsByTagName",
    , "js_method_alert", "js_method_eval",
    , "js_method_confirm",
    , "js_min_function_calls",
    , "html_length",
]
LABEL_MAP = {0: "Normal (Benign)", 1: "XSS Attack"}
def load_config(config_path=None):
    if config_path is None:
        config_path = PROJECT_ROOT / "config" / "config.yaml"
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config
def setup_logging(level=logging.INFO):
    logger = logging.getLogger("xss_detection")
    if logger.handlers:
        return logger
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(
        ,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)
