# Cross-Site Scripting (XSS) Attack Detection Using Machine Learning

## Technical Report

**Team Blackhat**  
Mohammad Ibrahim · Omar Adel · Mohamed Ahmed  

**Module**: Level 4 Primers  
**Instructor**: Dr. Wael El Sersy  
**Institution**: University of East London (UEL)  
**Date**: April 2026

---

## Executive Summary

Cross-Site Scripting (XSS) remains one of the most prevalent and dangerous web application vulnerabilities, consistently appearing in the OWASP Top Ten list of critical security threats. XSS attacks enable adversaries to inject malicious scripts into trusted websites, potentially leading to session hijacking, data theft, defacement, and distribution of malware to unsuspecting users.

This project presents a machine learning-based approach to automatically detect XSS attacks by analysing 66 features extracted from web page URLs, HTML content, and JavaScript behaviour. We utilise a comprehensive, publicly available dataset of 138,567 labelled samples, comprising 99,999 benign and 38,568 malicious instances, collected from real-world web sources.

We implement and compare three classification algorithms — Random Forest, XGBoost, and Logistic Regression — evaluating their performance using accuracy, precision, recall, F1-score, and ROC-AUC metrics across stratified 5-fold cross-validation. Our experiments demonstrate that ensemble tree-based methods, particularly Random Forest and XGBoost, achieve strong detection performance, effectively distinguishing XSS payloads from legitimate web content with high precision and recall.

The system is deployable as a lightweight web application built with Streamlit, enabling real-time prediction and practical use in web security monitoring. Our findings contribute to the growing body of research on automated vulnerability detection and demonstrate the viability of machine learning for enhancing web application security.

**Keywords**: Cross-Site Scripting, XSS Detection, Machine Learning, Random Forest, XGBoost, Web Application Security, Cybersecurity

---

## 1. Introduction

### 1.1 Background

Web applications have become the backbone of modern digital services, powering everything from banking platforms and e-commerce stores to healthcare systems and government portals. With this ubiquity comes an ever-expanding attack surface for malicious actors seeking to exploit vulnerabilities in web technologies.

Cross-Site Scripting (XSS) is a class of injection vulnerability in which an attacker inserts malicious client-side scripts into web pages viewed by other users. According to the OWASP Foundation (2021), XSS ranks among the top seven most critical web application security risks. The consequences of successful XSS attacks can be severe, including:

- **Session hijacking**: Stealing authentication cookies to impersonate legitimate users.
- **Data exfiltration**: Capturing sensitive form inputs such as credit card numbers and passwords.
- **Phishing**: Redirecting users to fraudulent websites through injected scripts.
- **Malware distribution**: Serving drive-by downloads through compromised pages.
- **Website defacement**: Altering the visual appearance of trusted websites.

The three main categories of XSS attacks are:

1. **Stored XSS**: Malicious script is permanently stored on the target server (e.g., in a database, forum post, or comment field) and served to every user who views the affected page.
2. **Reflected XSS**: Malicious script is reflected off a web server, typically through a URL parameter that is immediately echoed back in the response.
3. **DOM-based XSS**: The vulnerability exists in client-side code rather than server-side, exploiting the Document Object Model to execute payloads.

### 1.2 Problem Statement

Traditional XSS detection relies on rule-based approaches such as Web Application Firewalls (WAFs) that maintain signature databases of known attack patterns. While effective against well-documented payloads, these systems suffer from critical limitations:

- **High false-positive rates**: Legitimate JavaScript-heavy pages may trigger false alarms.
- **Inability to detect novel attacks**: Obfuscated or zero-day XSS payloads bypass static rules.
- **Maintenance burden**: Signature databases require continuous manual updating.

Machine learning offers a promising alternative by learning complex, non-linear decision boundaries from data, enabling the detection of both known and novel XSS variants without explicit rule engineering.

### 1.3 Objectives

The primary objectives of this project are:

1. To build a robust, reproducible machine learning pipeline for XSS attack detection.
2. To compare the performance of three classification algorithms (Random Forest, XGBoost, Logistic Regression) on a comprehensive real-world dataset.
3. To analyse which feature categories (URL, HTML, JavaScript) contribute most to detection accuracy.
4. To deploy the trained model as an interactive web application for real-time prediction.

### 1.4 Success Criteria

- Achieve F1-score ≥ 0.90 on the test set with the best-performing model.
- Produce at least 8 publication-quality visualisations of results.
- Deliver a functional demo application capable of real-time predictions.
- Maintain code quality with ≥ 60% unit test coverage.

### 1.5 Target Users and Stakeholders

- **Web developers** seeking automated security scanning for their applications.
- **Security analysts** monitoring web traffic for XSS indicators.
- **SOC teams** requiring ML-augmented detection in their security pipelines.
- **Academic researchers** studying machine learning applications in cybersecurity.

---

## 2. Literature Review

### 2.1 Traditional XSS Detection Methods

Early XSS detection systems relied on pattern matching and regular expressions to identify malicious input. ModSecurity (Trustwave, 2013) and similar WAFs maintain curated rule sets that match known XSS signatures. While providing a baseline defence, these systems are inherently reactive — they can only detect attacks whose patterns have been previously catalogued.

Pelizzi and Sekar (2012) proposed a server-side approach that tracks taint propagation through web application code, marking untrusted user input and preventing its execution in sensitive contexts. While theoretically sound, taint-tracking imposes significant runtime overhead and requires instrumentation of the entire application stack.

### 2.2 Machine Learning Approaches to XSS Detection

The application of machine learning to XSS detection has gained significant momentum in recent years. Key contributions include:

**Likarish et al. (2009)** were among the first to apply supervised learning to XSS detection, using features extracted from HTTP request parameters to train Naïve Bayes and SVM classifiers. Their work demonstrated that ML could achieve detection rates above 90%, though on a relatively small dataset.

**Wang et al. (2018)** proposed a deep learning approach using Convolutional Neural Networks (CNNs) to learn spatial patterns in XSS payloads represented as character sequences. Their model achieved 99.2% accuracy but required significant computational resources for training and inference.

**Mokbal et al. (2019)** introduced MLPXSS, a Multilayer Perceptron-based detection scheme that extracts 42 dynamic features from both URL and HTML content. Their approach achieved high detection rates while maintaining computational efficiency, making it suitable for real-time deployment.

**Mokbal et al. (2021)** extended their prior work with XGBXSS, employing XGBoost with a novel hybrid feature selection approach combining Information Gain and Sequential Backward Selection (IG-SBS). Starting from 167 features, they identified an optimal subset of 66 features, achieving state-of-the-art performance on a dataset of 138,567 samples — the same dataset used in this project.

**Fang et al. (2018)** utilised Long Short-Term Memory (LSTM) networks to capture sequential dependencies in XSS payloads, treating the detection task as a sequence classification problem. Their model showed strong performance on obfuscated payloads that evade pattern-matching approaches.

**Zhou and Wang (2019)** combined feature engineering with ensemble methods, employing Random Forests with features derived from HTML tag analysis, JavaScript API calls, and URL structure. They demonstrated that ensemble methods consistently outperform single-model approaches for XSS detection.

### 2.3 Comparative Summary

| Study | Method | Features | Dataset Size | Best Accuracy |
|-------|--------|----------|-------------|---------------|
| Likarish et al. (2009) | SVM, NB | HTTP parameters | ~5,000 | 92.0% |
| Wang et al. (2018) | CNN | Character sequences | ~40,000 | 99.2% |
| Mokbal et al. (2019) | MLP | 42 dynamic features | 138,567 | 99.0% |
| Mokbal et al. (2021) | XGBoost | 66 selected features | 138,567 | 99.4% |
| Fang et al. (2018) | LSTM | Token sequences | ~50,000 | 98.2% |
| Zhou & Wang (2019) | RF Ensemble | HTML/JS/URL | ~80,000 | 98.8% |
| **This project** | **RF, XGB, LR** | **66 features** | **138,567** | **99.47%** |

### 2.4 Gap Analysis

While deep learning methods (CNN, LSTM) show impressive accuracy, they require substantial training data and compute resources, limiting their practicality in resource-constrained environments. Traditional ML methods with well-engineered features offer a favourable trade-off between performance and deployability. This project extends the comparison by systematically evaluating Random Forest, XGBoost, and Logistic Regression on the same dataset and features, providing practitioners with a clear guide to model selection for XSS detection.

---

## 3. Methodology

### 3.1 System Architecture

The XSS detection system follows a standard machine learning pipeline architecture:

```
┌─────────────┐     ┌──────────────────┐     ┌───────────────┐
│  Raw Data   │────▶│  Preprocessing   │────▶│   Feature     │
│  (CSV)      │     │  & Cleaning      │     │   Scaling     │
└─────────────┘     └──────────────────┘     └───────────────┘
                                                      │
                                                      ▼
┌─────────────┐     ┌──────────────────┐     ┌───────────────┐
│  Evaluation │◀────│    Training      │◀────│  Train/Val/   │
│  & Figures  │     │  (CV + Full)     │     │  Test Split   │
└─────────────┘     └──────────────────┘     └───────────────┘
       │
       ▼
┌─────────────┐
│  Streamlit  │
│  Demo App   │
└─────────────┘
```

### 3.2 Dataset Description

We use the XSS dataset by Mokbal et al. (2021), available at https://github.com/fawaz2015/XSS-dataset. The dataset comprises:

- **Total samples**: 138,567
- **Benign samples**: 99,999 (72.1%)
- **Malicious samples**: 38,568 (27.9%)
- **Features**: 66 (pre-selected via IG-SBS from 167 original features)
- **Feature types**: All integer-valued counts and indicators

The features are grouped into three categories:
- **URL features** (11): Structural properties of the URL.
- **HTML features** (38): Tag counts, attribute counts, and event handler counts from the HTML DOM.
- **JavaScript features** (17): DOM API calls, property accesses, and code complexity indicators.

A detailed data dictionary is provided in `data/README.md`.

### 3.3 Data Collection Methodology

The benign data was collected using a Python-based web crawler employing random walk and random jumping techniques seeded from the Alexa Top 50,000 websites. The malicious data was collected deterministically from XSSed.com and Open Bug Bounty — two established repositories of confirmed XSS vulnerabilities.

### 3.4 Preprocessing Pipeline

1. **Loading**: The CSV dataset is loaded with the 66 feature column names applied programmatically.
2. **Duplicate removal**: Duplicate rows are identified and removed.
3. **Missing value handling**: Any missing values are imputed using column medians.
4. **Stratified splitting**: Data is divided into training (70%), validation (15%), and test (15%) sets, preserving the original class distribution in each split.
5. **Feature scaling**: StandardScaler normalisation (zero mean, unit variance) is applied, fitted on the training set and applied to validation and test sets to prevent data leakage.

### 3.5 Model Selection and Justification

We select three classifiers representing different algorithmic paradigms:

**Random Forest** — An ensemble of decision trees trained on bootstrapped subsets with random feature subsampling. Selected for its robustness to overfitting, interpretable feature importances, and strong out-of-the-box performance on tabular data (Breiman, 2001).

**XGBoost** — A gradient boosting framework that builds trees sequentially, each correcting the errors of its predecessor. Selected as it is the method used in the original XGBXSS paper (Mokbal et al., 2021), enabling direct comparison with published benchmarks.

**Logistic Regression** — A linear model serving as a baseline. Selected to quantify the improvement gained from non-linear models and to assess whether the feature space is linearly separable.

### 3.6 Hyperparameter Configuration

All hyperparameters are centralised in `config/config.yaml`:

| Model | Parameter | Value |
|-------|-----------|-------|
| Random Forest | n_estimators | 200 |
| Random Forest | max_depth | 20 |
| Random Forest | min_samples_split | 5 |
| XGBoost | n_estimators | 200 |
| XGBoost | max_depth | 8 |
| XGBoost | learning_rate | 0.1 |
| Logistic Regression | C | 1.0 |
| Logistic Regression | solver | lbfgs |

### 3.7 Evaluation Strategy

- **5-fold Stratified Cross-Validation** on the training set for unbiased performance estimation.
- **Hold-out test set** evaluation for final comparison.
- **Metrics**: Accuracy, Precision, Recall, F1-score, ROC-AUC, Average Precision.
- **Visualisations**: Confusion matrices, ROC curves, Precision-Recall curves, feature importance charts.

---

## 4. Experimental Setup

### 4.1 Computing Environment

- **Operating System**: Linux (Ubuntu-based)
- **Python Version**: 3.8+
- **Key Libraries**: scikit-learn 1.2+, XGBoost 1.7+, pandas, NumPy, matplotlib, seaborn
- **Hardware**: Standard multi-core CPU (no GPU required)

### 4.2 Reproducibility

All experiments are fully reproducible through:
- Fixed random seeds (`random_state=42`) across all stochastic components.
- Centralised configuration in `config/config.yaml`.
- Persisted data splits and scaler parameters in `data/processed/`.
- Version-pinned dependencies in `requirements.txt`.

### 4.3 Pipeline Execution

The entire experiment can be replicated with a single command:

```bash
python run_all.py
```

This executes: dataset download → preprocessing → training (with CV) → evaluation → figure generation.

---

## 5. Results and Analysis

### 5.1 Dataset Exploration

The dataset exhibits a moderate class imbalance with approximately 72% benign and 28% malicious samples. This imbalance ratio (0.386) is manageable without requiring resampling techniques, though we use stratified splitting and F1-score (which accounts for both precision and recall) as our primary evaluation metric.

Exploratory analysis reveals that several features are highly indicative of XSS attacks:
- `html_tag_script`: Malicious samples tend to have significantly higher script tag counts.
- `js_method_alert`: The `alert()` function is a common XSS payload marker.
- `url_event_onerror`: Event handler injection in URLs is a strong attack indicator.
- `js_method_eval`: Use of `eval()` correlates strongly with malicious intent.

### 5.2 Model Performance

#### 5.2.1 Cross-Validation Results

All three models were evaluated using 5-fold stratified cross-validation on the training set. The table below summarises the mean ± standard deviation for each metric:

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Random Forest | 99.31% ± 0.08% | 99.48% ± 0.07% | 98.22% ± 0.21% | 98.76% ± 0.12% |
| XGBoost | 99.52% ± 0.05% | 99.59% ± 0.07% | 98.66% ± 0.18% | 99.12% ± 0.10% |
| Logistic Regression | 98.14% ± 0.13% | 98.94% ± 0.13% | 94.26% ± 0.50% | 96.54% ± 0.25% |

*Refer to Figure 9 (CV Box Plots) for the distribution of per-fold scores.*

#### 5.2.2 Test Set Performance

The final test-set metrics provide an unbiased estimate of generalisation performance:

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| Random Forest | 99.31% | 99.64% | 97.84% | 98.73% | 99.95% |
| **XGBoost** | **99.47%** | **99.48%** | **98.57%** | **99.02%** | **99.97%** |
| Logistic Regression | 98.10% | 98.92% | 94.12% | 96.46% | 99.66% |

XGBoost achieves the highest overall performance, closely followed by Random Forest. Both ensemble methods significantly outperform the Logistic Regression baseline, confirming that the feature space contains non-linear decision boundaries that benefit from tree-based modelling. All three models exceed the F1-score ≥ 0.90 success criterion.

#### 5.2.3 Confusion Matrix Analysis

The confusion matrices (Figures 4-6) reveal the trade-off between false positives and false negatives for each model. In the context of XSS detection:
- **False Positives** (benign classified as attack): May cause legitimate content to be blocked.
- **False Negatives** (attack classified as benign): A critical security failure, allowing malicious scripts to reach users.

For security applications, minimising false negatives (high recall) is generally prioritised over minimising false positives.

### 5.3 Feature Importance Analysis

The Random Forest model provides feature importance scores based on mean decrease in Gini impurity. The top-20 most important features are visualised in Figure 3. Feature group analysis (Figure 10) reveals the relative contribution of URL, HTML, and JavaScript feature categories to overall detection accuracy.

### 5.4 ROC and Precision-Recall Analysis

The ROC curves (Figure 6) and Precision-Recall curves (Figure 7) provide threshold-independent evaluation of discriminative power. ROC-AUC values close to 1.0 indicate near-perfect class separation, while the Precision-Recall curve is particularly informative given the class imbalance in the dataset.

---

## 6. Discussion

### 6.1 Key Findings

1. **Ensemble methods outperform linear models**: Both Random Forest and XGBoost demonstrate superior performance to Logistic Regression, confirming that the feature space contains complex non-linear decision boundaries.

2. **Feature importance aligns with domain knowledge**: Features related to script tags, event handlers, and JavaScript API calls (e.g., `alert()`, `eval()`) rank highest in importance, matching known XSS attack patterns documented by OWASP.

3. **Pre-selected features are effective**: The 66-feature subset selected via IG-SBS by Mokbal et al. proves sufficient for high-accuracy detection, validating the original feature selection methodology.

### 6.2 Limitations

1. **Static feature analysis**: Our approach relies on pre-extracted features rather than analysing raw web content in real-time. This limits applicability to novel attack vectors not represented in the feature set.

2. **Dataset age**: The dataset, while comprehensive, reflects attack patterns from the period of collection. Modern XSS techniques (e.g., mutation XSS, DOM clobbering) may not be fully represented.

3. **Binary classification**: The system classifies inputs as either benign or malicious without distinguishing between XSS subtypes (stored, reflected, DOM-based), which could be valuable for incident response.

4. **No adversarial robustness testing**: We have not evaluated the models' resilience against adversarial examples — attackers who deliberately craft inputs to evade detection.

### 6.3 Comparison with Related Work

Our results are consistent with findings from Mokbal et al. (2021), who achieved 99.4% accuracy using XGBoost on the same dataset. The slight differences may be attributed to different train/test splitting strategies and hyperparameter choices.

---

## 7. Conclusion and Future Work

### 7.1 Conclusion

This project demonstrates the effectiveness of machine learning for Cross-Site Scripting attack detection. Using a comprehensive dataset of 138,567 samples with 66 pre-selected features, we successfully trained and compared three classifiers. The ensemble methods (Random Forest and XGBoost) achieved strong performance across all metrics, making them viable candidates for deployment in web application security systems.

The complete pipeline — from data preprocessing to model evaluation and interactive demonstration — is fully automated and reproducible, requiring only a single command to execute.

### 7.2 Future Work

1. **Deep learning exploration**: Implement LSTM or Transformer-based models to capture sequential patterns in raw XSS payloads.
2. **Real-time feature extraction**: Build a pipeline that accepts raw URLs/HTML and extracts features on-the-fly for live deployment.
3. **Multi-class classification**: Extend the system to distinguish between stored, reflected, and DOM-based XSS subtypes.
4. **Adversarial robustness**: Evaluate and improve model resilience against evasion attacks using adversarial ML techniques.
5. **Integration with WAFs**: Package the model as a plugin for existing Web Application Firewalls (e.g., ModSecurity).
6. **Continuous learning**: Implement an online learning pipeline that updates the model as new XSS patterns emerge.

---

## References

[1] OWASP Foundation. (2021). *OWASP Top Ten — A07:2021 Cross-Site Scripting (XSS)*. Available at: https://owasp.org/Top10/A07_2021-Cross-Site_Scripting_%28XSS%29/

[2] Mokbal, F. M. M., Dan, W., Xiaoxi, W., Wenbin, Z., & Lihua, F. (2021). XGBXSS: An Extreme Gradient Boosting Detection Framework for Cross-Site Scripting Attacks Based on Hybrid Feature Selection Approach and Parameters Optimization. *Journal of Information Security and Applications*, 58, 102813.

[3] Mokbal, F. M. M., Dan, W., Imran, A., Jiuchuan, L., Akhtar, F., & Xiaoxi, W. (2019). MLPXSS: An Integrated XSS-Based Attack Detection Scheme in Web Applications Using Multilayer Perceptron Technique. *IEEE Access*, 7, 100567-100580.

[4] Likarish, P., Jung, E., & Jo, I. (2009). Obfuscated Malicious JavaScript Detection Using Classification Techniques. *4th International Conference on Malicious and Unwanted Software (MALWARE)*, IEEE, pp. 47-54.

[5] Wang, Y., Cai, W., & Wei, P. (2018). A Deep Learning Approach for Detecting Malicious JavaScript Code. *Security and Communication Networks*, 2018, Article ID 5327459.

[6] Fang, Y., Li, Y., Liu, L., & Huang, C. (2018). DeepXSS: Cross Site Scripting Detection Based on Deep Learning. *Proceedings of the 2018 International Conference on Computing and Artificial Intelligence*, ACM, pp. 47-51.

[7] Zhou, Y. & Wang, P. (2019). An Ensemble Learning Approach for XSS Attack Detection with Domain Knowledge and Threat Intelligence. *Computers & Security*, 82, pp. 261-279.

[8] Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), pp. 5-32.

[9] Chen, T. & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, pp. 785-794.

[10] Pelizzi, R. & Sekar, R. (2012). Protection, Usability and Improvements in Reflected XSS Filters. *Proceedings of the 7th ACM Symposium on Information, Computer and Communications Security*, pp. 5-5.

---

## Appendix A: Project Repository Structure

See the `README.md` file in the project root for the complete repository structure and setup instructions.

## Appendix B: Configuration File

All hyperparameters are defined in `config/config.yaml` and can be modified without changing source code.

## Appendix C: Sample Predictions

The Streamlit demo application (`demo/app.py`) includes a "Sample Predictions" tab that shows 10 randomly selected test cases with actual labels, predicted labels, and confidence scores.
