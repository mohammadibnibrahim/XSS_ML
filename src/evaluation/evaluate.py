"""
evaluate.py — Model evaluation, metrics computation, and visualisation.

Generates all required plots (8+ figures) and computes comprehensive
classification metrics for each trained model.

Authors: Mohammad Ibrahim, Omar Adel, Mohamed Ahmed
Team: Blackhat — University of East London
Module: Level 4 Primers (Dr. Wael El Sersy)
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for server/CI environments
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, auc,
    precision_recall_curve, average_precision_score,
)

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.utils.helpers import (
    load_config, setup_logging, ensure_dir, PROJECT_ROOT, LABEL_MAP,
)

logger = setup_logging()

# ── Plotting style ─────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
})


def compute_metrics(y_true, y_pred, y_prob=None):
    """
    Compute a full set of classification metrics.

    Parameters
    ----------
    y_true : array-like
        Ground-truth labels.
    y_pred : array-like
        Predicted labels.
    y_prob : array-like, optional
        Predicted probabilities for the positive class (class 1).

    Returns
    -------
    dict
        Dictionary of metric_name -> value.
    """
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1_score": f1_score(y_true, y_pred, zero_division=0),
    }

    if y_prob is not None:
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        metrics["roc_auc"] = auc(fpr, tpr)
        metrics["avg_precision"] = average_precision_score(y_true, y_prob)

    return metrics


def plot_class_distribution(y, save_dir):
    """
    Figure 1: Class distribution bar chart.
    """
    fig, ax = plt.subplots(figsize=(7, 5))
    classes, counts = np.unique(y, return_counts=True)
    labels = [LABEL_MAP.get(c, str(c)) for c in classes]
    colors = ["#2ecc71", "#e74c3c"]

    bars = ax.bar(labels, counts, color=colors, edgecolor="white", linewidth=1.2)

    for bar, count in zip(bars, counts):
        pct = count / sum(counts) * 100
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 500,
                f"{count:,}\n({pct:.1f}%)", ha="center", va="bottom", fontweight="bold")

    ax.set_title("Class Distribution in XSS Dataset", fontweight="bold")
    ax.set_ylabel("Number of Samples")
    ax.set_xlabel("Class")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_dir / "01_class_distribution.png")
    plt.close()
    logger.info("Saved: 01_class_distribution.png")


def plot_correlation_heatmap(corr_matrix, save_dir):
    """
    Figure 2: Feature correlation heatmap.
    """
    fig, ax = plt.subplots(figsize=(16, 14))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

    sns.heatmap(
        corr_matrix, mask=mask, cmap="coolwarm", center=0,
        square=True, linewidths=0.1, ax=ax,
        cbar_kws={"shrink": 0.8, "label": "Pearson Correlation"},
        xticklabels=True, yticklabels=True,
    )
    ax.set_title("Feature Correlation Heatmap (66 Features)", fontweight="bold", pad=15)
    ax.tick_params(axis="both", labelsize=5)
    plt.tight_layout()
    plt.savefig(save_dir / "02_correlation_heatmap.png")
    plt.close()
    logger.info("Saved: 02_correlation_heatmap.png")


def plot_feature_importance(importance_df, save_dir, top_n=20):
    """
    Figure 3: Top-N feature importance (horizontal bar chart).
    """
    top = importance_df.head(top_n).iloc[::-1]  # Reverse for horizontal bar
    fig, ax = plt.subplots(figsize=(9, 8))

    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(top)))
    ax.barh(top["feature"], top["importance"], color=colors, edgecolor="white")

    ax.set_title(f"Top {top_n} Most Important Features (Random Forest)", fontweight="bold")
    ax.set_xlabel("Importance Score")
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_dir / "03_feature_importance.png")
    plt.close()
    logger.info("Saved: 03_feature_importance.png")


def plot_confusion_matrix(y_true, y_pred, model_name, save_dir, fig_num):
    """
    Figures 4-5: Confusion matrix heatmaps for individual models.
    """
    cm = confusion_matrix(y_true, y_pred)
    labels = [LABEL_MAP[0], LABEL_MAP[1]]

    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(
        cm, annot=True, fmt=",d", cmap="Blues",
        xticklabels=labels, yticklabels=labels, ax=ax,
        linewidths=1, linecolor="white",
        annot_kws={"size": 14, "fontweight": "bold"},
    )
    ax.set_title(f"Confusion Matrix — {model_name}", fontweight="bold")
    ax.set_ylabel("Actual Label")
    ax.set_xlabel("Predicted Label")
    plt.tight_layout()

    filename = f"{fig_num:02d}_confusion_matrix_{model_name.lower().replace(' ', '_')}.png"
    plt.savefig(save_dir / filename)
    plt.close()
    logger.info(f"Saved: {filename}")


def plot_roc_curves(model_results, X_test, y_test, save_dir):
    """
    Figure 6: ROC curves comparison for all models.
    """
    fig, ax = plt.subplots(figsize=(8, 7))
    colors = ["#3498db", "#e74c3c", "#2ecc71"]

    for (name, result), color in zip(model_results.items(), colors):
        model = result["model"]
        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test)[:, 1]
        else:
            y_prob = model.decision_function(X_test)

        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)

        ax.plot(fpr, tpr, color=color, linewidth=2,
                label=f"{name} (AUC = {roc_auc:.4f})")

    ax.plot([0, 1], [0, 1], "k--", alpha=0.5, linewidth=1, label="Random Baseline")
    ax.set_title("ROC Curve Comparison", fontweight="bold")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.legend(loc="lower right", fontsize=10)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_dir / "06_roc_curves_comparison.png")
    plt.close()
    logger.info("Saved: 06_roc_curves_comparison.png")


def plot_precision_recall_curves(model_results, X_test, y_test, save_dir):
    """
    Figure 7: Precision-Recall curves comparison.
    """
    fig, ax = plt.subplots(figsize=(8, 7))
    colors = ["#3498db", "#e74c3c", "#2ecc71"]

    for (name, result), color in zip(model_results.items(), colors):
        model = result["model"]
        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test)[:, 1]
        else:
            y_prob = model.decision_function(X_test)

        precision, recall, _ = precision_recall_curve(y_test, y_prob)
        ap = average_precision_score(y_test, y_prob)

        ax.plot(recall, precision, color=color, linewidth=2,
                label=f"{name} (AP = {ap:.4f})")

    ax.set_title("Precision-Recall Curve Comparison", fontweight="bold")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.legend(loc="lower left", fontsize=10)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_dir / "07_precision_recall_curves.png")
    plt.close()
    logger.info("Saved: 07_precision_recall_curves.png")


def plot_model_comparison(all_metrics, save_dir):
    """
    Figure 8: Model comparison bar chart (grouped bars for all metrics).
    """
    df = pd.DataFrame(all_metrics).T
    metrics_to_plot = ["accuracy", "precision", "recall", "f1_score", "roc_auc"]
    df_plot = df[metrics_to_plot]

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(df_plot.columns))
    width = 0.25
    colors = ["#3498db", "#e74c3c", "#2ecc71"]

    for i, (model_name, row) in enumerate(df_plot.iterrows()):
        bars = ax.bar(x + i * width, row.values, width,
                      label=model_name, color=colors[i], edgecolor="white")
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 0.005,
                    f"{height:.3f}", ha="center", va="bottom", fontsize=8)

    ax.set_title("Model Performance Comparison", fontweight="bold")
    ax.set_ylabel("Score")
    ax.set_xticks(x + width)
    ax.set_xticklabels([m.replace("_", " ").title() for m in metrics_to_plot])
    ax.legend(fontsize=10)
    ax.set_ylim(0, 1.1)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_dir / "08_model_comparison.png")
    plt.close()
    logger.info("Saved: 08_model_comparison.png")


def plot_cv_boxplots(model_results, save_dir):
    """
    Figure 9: Cross-validation performance distribution (box plots).
    """
    fig, axes = plt.subplots(1, 4, figsize=(16, 5))
    metrics = ["accuracy", "precision", "recall", "f1"]
    colors = ["#3498db", "#e74c3c", "#2ecc71"]

    for ax, metric in zip(axes, metrics):
        data = []
        labels = []
        for name, result in model_results.items():
            key = f"test_{metric}"
            data.append(result["cv_results"][key])
            labels.append(name)

        bp = ax.boxplot(data, labels=labels, patch_artist=True)
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        ax.set_title(metric.title(), fontweight="bold")
        ax.grid(axis="y", alpha=0.3)
        ax.tick_params(axis="x", rotation=30, labelsize=8)

    fig.suptitle("Cross-Validation Performance Distribution (5-Fold)",
                 fontweight="bold", fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(save_dir / "09_cv_boxplots.png", bbox_inches="tight")
    plt.close()
    logger.info("Saved: 09_cv_boxplots.png")


def plot_feature_group_analysis(group_df, save_dir):
    """
    Figure 10: Feature group importance comparison (URL vs HTML vs JS).
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["#3498db", "#e74c3c", "#f39c12", "#9b59b6"]

    bars = ax.bar(group_df["group"], group_df["total_importance"],
                  color=colors[:len(group_df)], edgecolor="white", linewidth=1.2)

    for bar, val in zip(bars, group_df["total_importance"]):
        pct = val * 100
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                f"{pct:.1f}%", ha="center", va="bottom", fontweight="bold")

    ax.set_title("Feature Group Importance Analysis", fontweight="bold")
    ax.set_ylabel("Total Importance")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_dir / "10_feature_group_analysis.png")
    plt.close()
    logger.info("Saved: 10_feature_group_analysis.png")


def generate_comparison_table(all_metrics):
    """
    Build a formatted comparison table of all model metrics.

    Parameters
    ----------
    all_metrics : dict
        Mapping model_name -> metrics dict.

    Returns
    -------
    pd.DataFrame
        Formatted comparison table.
    """
    df = pd.DataFrame(all_metrics).T
    df.index.name = "Model"
    logger.info(f"\n{'='*60}\nModel Comparison Table\n{'='*60}\n{df.to_string()}\n{'='*60}")
    return df


def evaluate_all_models(model_results, data, config):
    """
    Run full evaluation pipeline: compute metrics, generate all 10 figures.

    Parameters
    ----------
    model_results : dict
        Mapping model_name -> {'model': fitted, 'cv_results': dict}.
    data : dict
        Preprocessed data.
    config : dict
        Project configuration.

    Returns
    -------
    dict
        Mapping model_name -> metrics dict.
    """
    fig_dir = PROJECT_ROOT / config["output"]["figures_dir"]
    ensure_dir(fig_dir)

    X_test = data["X_test"]
    y_test = data["y_test"]
    feature_names = data["feature_names"]

    # ── Figure 1: Class distribution ────────────────────────────────
    y_all = np.concatenate([data["y_train"], data["y_val"], data["y_test"]])
    plot_class_distribution(y_all, fig_dir)

    # ── Figure 2: Correlation heatmap ───────────────────────────────
    from src.feature_engineering.features import (
        compute_correlation_matrix, get_feature_importance, analyse_feature_groups,
    )
    corr = compute_correlation_matrix(data["X_train"], feature_names)
    plot_correlation_heatmap(corr, fig_dir)

    # ── Compute test-set metrics for all models ─────────────────────
    all_metrics = {}
    fig_num = 4

    for name, result in model_results.items():
        model = result["model"]
        y_pred = model.predict(X_test)

        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test)[:, 1]
        else:
            y_prob = None

        metrics = compute_metrics(y_test, y_pred, y_prob)
        all_metrics[name] = metrics

        # Print classification report
        logger.info(f"\n{'='*50}\n{name} — Classification Report\n{'='*50}")
        logger.info("\n" + classification_report(
            y_test, y_pred, target_names=[LABEL_MAP[0], LABEL_MAP[1]]
        ))

        # ── Figures 4-5: Confusion matrices ─────────────────────────
        plot_confusion_matrix(y_test, y_pred, name, fig_dir, fig_num)
        fig_num += 1

    # ── Figure 3: Feature importance (from Random Forest) ───────────
    rf_model = model_results["Random Forest"]["model"]
    importance_df = get_feature_importance(rf_model, feature_names)
    plot_feature_importance(importance_df, fig_dir)

    # ── Figure 6: ROC curves ────────────────────────────────────────
    plot_roc_curves(model_results, X_test, y_test, fig_dir)

    # ── Figure 7: Precision-Recall curves ───────────────────────────
    plot_precision_recall_curves(model_results, X_test, y_test, fig_dir)

    # ── Figure 8: Model comparison bar chart ────────────────────────
    plot_model_comparison(all_metrics, fig_dir)

    # ── Figure 9: CV box plots ──────────────────────────────────────
    plot_cv_boxplots(model_results, fig_dir)

    # ── Figure 10: Feature group analysis ───────────────────────────
    group_df = analyse_feature_groups(importance_df)
    plot_feature_group_analysis(group_df, fig_dir)

    # ── Comparison table ────────────────────────────────────────────
    comparison = generate_comparison_table(all_metrics)
    comparison.to_csv(fig_dir / "model_comparison_table.csv")

    return all_metrics
