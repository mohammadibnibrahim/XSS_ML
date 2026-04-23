"""
helpers.py — Utility functions for the XSS Detection project.

Provides configuration loading, logging setup, and shared constants
used across all modules in the pipeline.

Authors: Mohammad Ibrahim, Omar Adel, Mohamed Ahmed
Team: Blackhat — University of East London
Module: Level 4 Primers (Dr. Wael El Sersy)
"""

import os
import yaml
import logging
from pathlib import Path


# ── Project root directory (two levels up from src/utils/) ──────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# ── Feature group definitions ──────────────────────────────────────────
# These groups correspond to the three major categories in the dataset,
# making it easier to analyse which signal source contributes most to
# XSS detection accuracy.

URL_FEATURES = [
    "url_length", "url_special_characters", "url_tag_script",
    "url_attr_action", "url_attr_src", "url_event_onerror",
    "url_event_onmouseover", "url_cookie", "url_number_keywords_param",
    "url_number_domain", "url_number_ip",
]

HTML_FEATURES = [
    "html_tag_script", "html_tag_iframe", "html_tag_meta",
    "html_tag_object", "html_tag_embed", "html_tag_link",
    "html_tag_svg", "html_tag_frame", "html_tag_form",
    "html_tag_div", "html_tag_style", "html_tag_img",
    "html_tag_input", "html_tag_textarea", "html_attr_action",
    "html_attr_background", "html_attr_codebase", "html_attr_data",
    "html_attr_href", "html_attr_longdesc", "html_attr_src",
    "html_attr_usemap", "html_attr_http-equiv", "html_event_onblur",
    "html_event_onchange", "html_event_onclick", "html_event_onerror",
    "html_event_onfocus", "html_event_onkeydown", "html_event_onkeypress",
    "html_event_onkeyup", "html_event_onload", "html_event_onmousedown",
    "html_event_onmouseout", "html_event_onmouseup", "html_event_onresize",
    "html_event_onsubmit", "html_number_keywords_evil",
]

JS_FEATURES = [
    "js_file", "js_pseudo_protocol", "js_dom_location",
    "js_dom_document", "js_prop_cookie", "js_prop_referrer",
    "js_method_write", "js_method_getElementsByTagName",
    "js_method_getElementById", "js_method_alert", "js_method_eval",
    "js_method_fromCharCode", "js_method_confirm",
    "js_min_define_function", "js_min_function_calls",
    "js_string_max_length", "html_length",
]

# Human-readable label mapping
LABEL_MAP = {0: "Normal (Benign)", 1: "XSS Attack"}


def load_config(config_path=None):
    """
    Load the YAML configuration file.

    Parameters
    ----------
    config_path : str or Path, optional
        Path to config.yaml.  Defaults to <project_root>/config/config.yaml.

    Returns
    -------
    dict
        Parsed configuration dictionary.
    """
    if config_path is None:
        config_path = PROJECT_ROOT / "config" / "config.yaml"

    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return config


def setup_logging(level=logging.INFO):
    """
    Configure a project-wide logger with consistent formatting.

    Parameters
    ----------
    level : int
        Logging level (e.g. logging.INFO, logging.DEBUG).

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    logger = logging.getLogger("xss_detection")
    if logger.handlers:
        # Already configured — avoid duplicate handlers
        return logger

    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setLevel(level)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def ensure_dir(path):
    """
    Create a directory (and parents) if it does not already exist.

    Parameters
    ----------
    path : str or Path
        Directory path to create.
    """
    Path(path).mkdir(parents=True, exist_ok=True)
