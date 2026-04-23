"""
app.py — Streamlit interactive demo for XSS Detection.

Provides a web interface where users can input feature values or
use pre-loaded test samples to see real-time XSS attack predictions
from the trained models.

Usage:
    streamlit run demo/app.py

Authors: Mohammad Ibrahim, Omar Adel, Mohamed Ahmed
Team: Blackhat — University of East London
Module: Level 4 Primers (Dr. Wael El Sersy)
"""

import streamlit as st
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
import sys

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.helpers import load_config, LABEL_MAP

# ── Page configuration ─────────────────────────────────────────────────
st.set_page_config(
    page_title="XSS Attack Detector — Team Blackhat",
    page_icon="🛡️",
    layout="wide",
)


@st.cache_resource
def load_models():
    """Load all trained models from disk."""
    models_dir = PROJECT_ROOT / "models"
    models = {}
    for path in sorted(models_dir.glob("*.joblib")):
        name = path.stem.replace("_", " ").title()
        models[name] = joblib.load(path)
    return models


@st.cache_resource
def load_scaler_and_features():
    """Load the scaler and feature names."""
    processed_dir = PROJECT_ROOT / "data" / "processed"
    scaler = joblib.load(processed_dir / "scaler.joblib")
    features = pd.read_csv(
        processed_dir / "feature_names.csv", header=None
    )[0].tolist()
    return scaler, features


@st.cache_data
def load_test_data():
    """Load test set for sample predictions."""
    processed_dir = PROJECT_ROOT / "data" / "processed"
    X_test = np.load(processed_dir / "X_test.npy")
    y_test = np.load(processed_dir / "y_test.npy")
    return X_test, y_test


def main():
    # ── Header ──────────────────────────────────────────────────────
    st.title("🛡️ XSS Attack Detection System")
    st.markdown(
        "**Team Blackhat** — University of East London  \n"
        "Level 4 Primers · Dr. Wael El Sersy"
    )
    st.markdown("---")

    # ── Load resources ──────────────────────────────────────────────
    try:
        models = load_models()
        scaler, feature_names = load_scaler_and_features()
        X_test, y_test = load_test_data()
    except Exception as e:
        st.error(
            f"Could not load models or data. "
            f"Please run `python run_all.py` first.\n\nError: {e}"
        )
        return

    # ── Sidebar ─────────────────────────────────────────────────────
    st.sidebar.title("⚙️ Settings")
    selected_model = st.sidebar.selectbox(
        "Select Model", list(models.keys())
    )
    model = models[selected_model]

    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "This system uses machine learning to detect Cross-Site "
        "Scripting (XSS) attacks by analysing 66 features extracted "
        "from web page URLs, HTML content, and JavaScript behaviour."
    )

    # ── Tabs ────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs([
        "🔍 Sample Predictions", "📊 Model Performance", "🧪 Manual Input"
    ])

    # ── Tab 1: Sample Predictions ───────────────────────────────────
    with tab1:
        st.subheader("Sample Test Predictions")
        st.markdown(
            "Showing predictions on **10 random test samples** "
            f"using the **{selected_model}** model."
        )

        # Select 10 random samples (seeded for reproducibility)
        np.random.seed(123)
        indices = np.random.choice(len(X_test), 10, replace=False)

        results = []
        for idx in indices:
            sample = X_test[idx].reshape(1, -1)
            pred = model.predict(sample)[0]
            prob = model.predict_proba(sample)[0] if hasattr(model, "predict_proba") else [0, 0]

            results.append({
                "Sample #": int(idx),
                "Actual": LABEL_MAP[int(y_test[idx])],
                "Predicted": LABEL_MAP[int(pred)],
                "Confidence": f"{max(prob) * 100:.1f}%",
                "Correct": "✅" if pred == y_test[idx] else "❌",
            })

        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)

        correct = sum(1 for r in results if r["Correct"] == "✅")
        st.success(f"Accuracy on these samples: {correct}/10 ({correct * 10}%)")

    # ── Tab 2: Model Performance ────────────────────────────────────
    with tab2:
        st.subheader("Model Performance on Test Set")

        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

        from src.evaluation.evaluate import compute_metrics
        metrics = compute_metrics(y_test, y_pred, y_prob)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Accuracy", f"{metrics['accuracy']:.4f}")
        col2.metric("Precision", f"{metrics['precision']:.4f}")
        col3.metric("Recall", f"{metrics['recall']:.4f}")
        col4.metric("F1 Score", f"{metrics['f1_score']:.4f}")

        if "roc_auc" in metrics:
            col1, col2 = st.columns(2)
            col1.metric("ROC-AUC", f"{metrics['roc_auc']:.4f}")
            col2.metric("Avg Precision", f"{metrics['avg_precision']:.4f}")

        # Show figures if they exist
        figures_dir = PROJECT_ROOT / "figures"
        if figures_dir.exists():
            st.markdown("### Generated Figures")
            figs = sorted(figures_dir.glob("*.png"))
            for fig_path in figs:
                st.image(str(fig_path), caption=fig_path.stem.replace("_", " ").title())

    # ── Tab 3: Manual Input ─────────────────────────────────────────
    with tab3:
        st.subheader("Manual Feature Input")
        st.markdown(
            "Enter feature values below to get a prediction.  "
            "Most features are integer counts (e.g. number of `<script>` tags)."
        )

        # Create input fields in columns
        cols = st.columns(3)
        input_values = []

        for i, feat in enumerate(feature_names):
            col = cols[i % 3]
            val = col.number_input(feat, value=0, step=1, key=f"feat_{i}")
            input_values.append(val)

        if st.button("🔍 Predict", type="primary"):
            sample = np.array(input_values).reshape(1, -1)
            sample_scaled = scaler.transform(sample)

            pred = model.predict(sample_scaled)[0]
            prob = model.predict_proba(sample_scaled)[0] if hasattr(model, "predict_proba") else None

            st.markdown("---")
            if pred == 1:
                st.error(f"⚠️ **XSS ATTACK DETECTED** (Confidence: {prob[1]*100:.1f}%)")
            else:
                st.success(f"✅ **Benign / Normal** (Confidence: {prob[0]*100:.1f}%)")


if __name__ == "__main__":
    main()
