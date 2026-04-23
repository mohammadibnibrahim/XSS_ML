# Dataset Documentation — XSS Detection

## Source Attribution

| Field | Detail |
|-------|--------|
| **Dataset Name** | Cross-site-scripting attacks: A Comprehensive dataset for AI techniques usage |
| **Authors** | Fawaz M. M. Mokbal, Wang Dan, Wang Xiaoxi, Zhang Wenbin, Fu Lihua |
| **Repository** | [github.com/fawaz2015/XSS-dataset](https://github.com/fawaz2015/XSS-dataset) |
| **License** | GPL-3.0 |
| **Size** | 138,567 samples (after deduplication: ~138,567) |
| **Features** | 66 pre-selected features + 1 class label |
| **Classes** | 0 = Normal/Benign (99,999 samples), 1 = XSS Attack (38,568 samples) |

## Data Collection Methodology

The dataset was constructed in two phases:

1. **Benign data**: Collected using a Python-based crawler employing a random walk and random jumping method. The crawler used the top 50,000 Alexa-ranked websites as initial seeds, crawling up to 150,000 webpages with 100 independent parallel walks. A uniform random sample of 100,000 webpages was then selected.

2. **Malicious data**: Collected deterministically from two sources — XSSed and Open Bug Bounty — yielding 38,569 malicious XSS samples.

## Feature Selection

The original dataset contains 167 features, extracted using dynamic-features extraction techniques. The 66-feature subset used in this project was obtained through the **Hybrid Feature Selection Approach (IG-SBS)** — Information Gain followed by Sequential Backward Selection — as proposed by Mokbal et al. (2021).

## Data Dictionary (66 Features)

### URL-Based Features (11 features)

| Feature | Type | Description |
|---------|------|-------------|
| `url_length` | int | Total length of the URL string |
| `url_special_characters` | int | Count of special characters in the URL |
| `url_tag_script` | int | Presence of `<script>` tag in URL |
| `url_attr_action` | int | Presence of `action` attribute in URL |
| `url_attr_src` | int | Presence of `src` attribute in URL |
| `url_event_onerror` | int | Presence of `onerror` event handler in URL |
| `url_event_onmouseover` | int | Presence of `onmouseover` event handler in URL |
| `url_cookie` | int | Reference to cookies in URL |
| `url_number_keywords_param` | int | Count of suspicious keywords in URL parameters |
| `url_number_domain` | int | Number of domain references in URL |
| `url_number_ip` | int | Number of IP addresses in URL |

### HTML-Based Features (38 features)

| Feature | Type | Description |
|---------|------|-------------|
| `html_tag_script` | int | Count of `<script>` tags in HTML |
| `html_tag_iframe` | int | Count of `<iframe>` tags |
| `html_tag_meta` | int | Count of `<meta>` tags |
| `html_tag_object` | int | Count of `<object>` tags |
| `html_tag_embed` | int | Count of `<embed>` tags |
| `html_tag_link` | int | Count of `<link>` tags |
| `html_tag_svg` | int | Count of `<svg>` tags |
| `html_tag_frame` | int | Count of `<frame>` tags |
| `html_tag_form` | int | Count of `<form>` tags |
| `html_tag_div` | int | Count of `<div>` tags |
| `html_tag_style` | int | Count of `<style>` tags |
| `html_tag_img` | int | Count of `<img>` tags |
| `html_tag_input` | int | Count of `<input>` tags |
| `html_tag_textarea` | int | Count of `<textarea>` tags |
| `html_attr_action` | int | Count of `action` attributes in HTML |
| `html_attr_background` | int | Count of `background` attributes |
| `html_attr_codebase` | int | Count of `codebase` attributes |
| `html_attr_data` | int | Count of `data` attributes |
| `html_attr_href` | int | Count of `href` attributes |
| `html_attr_longdesc` | int | Count of `longdesc` attributes |
| `html_attr_src` | int | Count of `src` attributes |
| `html_attr_usemap` | int | Count of `usemap` attributes |
| `html_attr_http-equiv` | int | Count of `http-equiv` attributes |
| `html_event_onblur` | int | Count of `onblur` event handlers |
| `html_event_onchange` | int | Count of `onchange` event handlers |
| `html_event_onclick` | int | Count of `onclick` event handlers |
| `html_event_onerror` | int | Count of `onerror` event handlers |
| `html_event_onfocus` | int | Count of `onfocus` event handlers |
| `html_event_onkeydown` | int | Count of `onkeydown` event handlers |
| `html_event_onkeypress` | int | Count of `onkeypress` event handlers |
| `html_event_onkeyup` | int | Count of `onkeyup` event handlers |
| `html_event_onload` | int | Count of `onload` event handlers |
| `html_event_onmousedown` | int | Count of `onmousedown` event handlers |
| `html_event_onmouseout` | int | Count of `onmouseout` event handlers |
| `html_event_onmouseup` | int | Count of `onmouseup` event handlers |
| `html_event_onresize` | int | Count of `onresize` event handlers |
| `html_event_onsubmit` | int | Count of `onsubmit` event handlers |
| `html_number_keywords_evil` | int | Count of suspicious/malicious keywords in HTML |

### JavaScript-Based Features (17 features)

| Feature | Type | Description |
|---------|------|-------------|
| `js_file` | int | Count of external JS file references |
| `js_pseudo_protocol` | int | Use of `javascript:` pseudo-protocol |
| `js_dom_location` | int | References to `window.location` |
| `js_dom_document` | int | References to `document` DOM object |
| `js_prop_cookie` | int | References to `document.cookie` |
| `js_prop_referrer` | int | References to `document.referrer` |
| `js_method_write` | int | Calls to `document.write()` |
| `js_method_getElementsByTagName` | int | Calls to `getElementsByTagName()` |
| `js_method_getElementById` | int | Calls to `getElementById()` |
| `js_method_alert` | int | Calls to `alert()` |
| `js_method_eval` | int | Calls to `eval()` |
| `js_method_fromCharCode` | int | Calls to `String.fromCharCode()` |
| `js_method_confirm` | int | Calls to `confirm()` |
| `js_min_define_function` | int | Minimum number of function definitions |
| `js_min_function_calls` | int | Minimum number of function calls |
| `js_string_max_length` | int | Maximum JavaScript string length |
| `html_length` | int | Total HTML content length |

### Target Variable

| Feature | Type | Description |
|---------|------|-------------|
| `class` | int | 0 = Normal/Benign, 1 = XSS Attack |

## Class Distribution

| Class | Label | Count | Percentage |
|-------|-------|-------|------------|
| 0 | Normal (Benign) | 99,999 | 72.1% |
| 1 | XSS Attack | 38,568 | 27.9% |

## References

1. Mokbal, F. M. M., Dan, W., Xiaoxi, W., Wenbin, Z., & Lihua, F. (2021). XGBXSS: An Extreme Gradient Boosting Detection Framework for Cross-Site Scripting Attacks Based on Hybrid Feature Selection Approach and Parameters Optimization. *Journal of Information Security and Applications*, 58, 102813.

2. Mokbal, F. M. M., Dan, W., Imran, A., Jiuchuan, L., Akhtar, F., & Xiaoxi, W. (2019). MLPXSS: An Integrated XSS-Based Attack Detection Scheme in Web Applications Using Multilayer Perceptron Technique. *IEEE Access*, 7, 100567-100580.
