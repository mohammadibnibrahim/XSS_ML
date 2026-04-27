import os
import yaml
import logging
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
URL_FEATURES = [
    "url_length", "url_number_special_characters", "url_special_characters", "url_tag_script",
    "url_tag_img", "url_attr_src", "url_event_onerror",
    "url_tag_script_embed", "url_cookie", "url_number_keywords_param",
    "url_number_dots", "url_number_ip",
]
HTML_FEATURES = [
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
]
JS_FEATURES = [
    "js_pseudo_protocol", "js_dom_location",
    "js_prop_cookie", "js_prop_referrer",
    "js_method_write", "js_method_getElementsByTagName",
    "js_method_alert", "js_method_eval",
    "js_method_setTimeout", "js_method_confirm",
    "js_method_prompt", "js_min_function_calls",
    "js_length", "html_length",
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
        "[%(asctime)s] %(levelname)-8s %(name)-12s -- %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)
