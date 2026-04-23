# XSS Attack Detection Using Machine Learning

> **Team Blackhat** — University of East London  
> Level 4 Primers · Dr. Wael El Sersy  
> Mohammad Ibrahim · Omar Adel · Mohamed Ahmed

## Overview

This project implements a machine learning pipeline to detect **Cross-Site Scripting (XSS) attacks** in web applications. Using a comprehensive dataset of 138,567 web page samples with 66 features extracted from URLs, HTML content, and JavaScript behaviour, we train and compare three classifiers:

- **Random Forest** (ensemble, tree-based)
- **XGBoost** (gradient boosting)
- **Logistic Regression** (linear baseline)

The system can classify web inputs as either **benign** or **XSS attack** with high accuracy, providing a practical tool for automated web application security.

## Dataset

We use the [XSS Dataset](https://github.com/fawaz2015/XSS-dataset) by Mokbal et al. — a comprehensive, pre-processed collection of 138,567 samples:

| Class | Samples | Percentage |
|-------|---------|------------|
| Normal (Benign) | 99,999 | 72.1% |
| XSS Attack | 38,568 | 27.9% |

See [`data/README.md`](data/README.md) for the complete data dictionary with all 66 features.

## Project Structure

```
project/
├── data/                        # Dataset files
│   ├── raw/                     # Original downloaded CSV
│   ├── processed/               # Train/val/test splits + scaler
│   └── README.md                # Data dictionary
├── src/                         # Source code modules
│   ├── preprocessing/           # Data loading & splitting
│   ├── feature_engineering/     # Feature analysis
│   ├── models/                  # Classifier definitions
│   ├── training/                # Training pipeline
│   ├── evaluation/              # Metrics & visualisation
│   └── utils/                   # Config, logging, constants
├── tests/                       # Unit tests
├── models/                      # Saved trained models (.joblib)
├── figures/                     # Generated plots (10 figures)
├── demo/                        # Streamlit web app
├── report/                      # Technical report
├── presentation/                # Slide generation script
├── config/config.yaml           # Hyperparameters & settings
├── requirements.txt             # Python dependencies
├── run_all.py                   # Master pipeline script
├── team_contribution.md         # Team contribution statement
├── LICENSE                      # MIT License
└── README.md                    # This file
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Full Pipeline

This single command downloads the dataset, preprocesses it, trains all three models, and generates all evaluation figures:

```bash
python run_all.py
```

### 3. Run Tests

```bash
pytest tests/ -v --cov=src
```

### 4. Launch the Demo App

```bash
streamlit run demo/app.py
```

The demo provides:
- Sample predictions on test data
- Model performance metrics and visualisations
- Manual feature input for real-time prediction

## Results

After training, the pipeline generates 10 publication-quality figures in `figures/`:

1. Class distribution chart
2. Feature correlation heatmap
3. Top-20 feature importance (Random Forest)
4. Confusion matrix (Random Forest)
5. Confusion matrix (XGBoost)
6. Confusion matrix (Logistic Regression)
7. ROC curve comparison
8. Precision-Recall curve comparison
9. Model comparison bar chart
10. Cross-validation box plots
11. Feature group importance analysis

A detailed comparison table is saved to `figures/model_comparison_table.csv`.

## Technologies Used

- **Python 3.8+**
- **scikit-learn** — Machine learning models and evaluation
- **XGBoost** — Gradient boosting implementation
- **pandas / NumPy** — Data manipulation
- **matplotlib / seaborn** — Visualisation
- **Streamlit** — Interactive demo application
- **pytest** — Unit testing

## References

1. Mokbal, F. M. M., Dan, W., Xiaoxi, W., Wenbin, Z., & Lihua, F. (2021). *XGBXSS: An Extreme Gradient Boosting Detection Framework for Cross-Site Scripting Attacks*. Journal of Information Security and Applications, 58, 102813.

2. Mokbal, F. M. M., Dan, W., Imran, A., Jiuchuan, L., Akhtar, F., & Xiaoxi, W. (2019). *MLPXSS: An Integrated XSS-Based Attack Detection Scheme in Web Applications Using Multilayer Perceptron Technique*. IEEE Access, 7, 100567-100580.

3. OWASP Foundation. (2021). *OWASP Top Ten — A07:2021 Cross-Site Scripting (XSS)*. https://owasp.org/Top10/A07_2021-Cross-Site_Scripting_%28XSS%29/

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.  
The dataset is licensed under GPL-3.0 — see the [dataset repository](https://github.com/fawaz2015/XSS-dataset) for details.
