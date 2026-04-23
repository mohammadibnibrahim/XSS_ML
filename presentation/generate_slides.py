"""
generate_slides.py — Automated PowerPoint presentation generator.

Creates a professional 18-slide presentation covering the XSS
Detection project: problem, methodology, results, and conclusions.

Usage:
    python presentation/generate_slides.py

Authors: Mohammad Ibrahim, Omar Adel, Mohamed Ahmed
Team: Blackhat — University of East London
Module: Level 4 Primers (Dr. Wael El Sersy)
"""

import os
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ── Colour palette ─────────────────────────────────────────────────────
DARK_BG = RGBColor(0x1A, 0x1A, 0x2E)
ACCENT_BLUE = RGBColor(0x00, 0xB4, 0xD8)
ACCENT_GREEN = RGBColor(0x2E, 0xCC, 0x71)
ACCENT_RED = RGBColor(0xE7, 0x4C, 0x3C)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xCC, 0xCC, 0xCC)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)


def set_slide_bg(slide, color=DARK_BG):
    """Set the background colour of a slide."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_text_box(slide, left, top, width, height, text, font_size=18,
                 bold=False, color=WHITE, alignment=PP_ALIGN.LEFT,
                 font_name="Calibri"):
    """Add a text box to a slide with styling."""
    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_bullet_list(slide, left, top, width, height, items,
                    font_size=16, color=WHITE):
    """Add a bulleted list to a slide."""
    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = "Calibri"
        p.space_after = Pt(6)
        p.level = 0

    return txBox


def add_image_safe(slide, img_path, left, top, width, height=None):
    """Add an image if it exists, otherwise add a placeholder box."""
    if Path(img_path).exists():
        if height:
            slide.shapes.add_picture(str(img_path), Inches(left), Inches(top),
                                     Inches(width), Inches(height))
        else:
            slide.shapes.add_picture(str(img_path), Inches(left), Inches(top),
                                     Inches(width))
    else:
        # Placeholder rectangle
        shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(left), Inches(top), Inches(width), Inches(height or 3)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(0x2C, 0x2C, 0x44)
        shape.line.color.rgb = ACCENT_BLUE
        tf = shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"[Figure: {Path(img_path).stem}]"
        p.font.size = Pt(12)
        p.font.color.rgb = LIGHT_GRAY
        p.alignment = PP_ALIGN.CENTER


def create_presentation():
    """Generate the full 18-slide presentation."""
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    fig_dir = PROJECT_ROOT / "figures"

    # ── Slide 1: Title ──────────────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
    set_slide_bg(slide)

    # Accent bar at top
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(0), Inches(13.333), Inches(0.08)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT_BLUE
    shape.line.fill.background()

    add_text_box(slide, 1.5, 1.5, 10, 1.5,
                 "XSS Attack Detection Using Machine Learning",
                 font_size=36, bold=True, color=WHITE,
                 alignment=PP_ALIGN.CENTER)

    add_text_box(slide, 1.5, 3.2, 10, 0.8,
                 "Cross-Site Scripting Detection with Random Forest, XGBoost & Logistic Regression",
                 font_size=18, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

    add_text_box(slide, 1.5, 4.5, 10, 0.6,
                 "Team Blackhat",
                 font_size=24, bold=True, color=ACCENT_BLUE,
                 alignment=PP_ALIGN.CENTER)

    add_text_box(slide, 1.5, 5.2, 10, 0.5,
                 "Mohammad Ibrahim  ·  Omar Adel  ·  Mohamed Ahmed",
                 font_size=16, color=WHITE, alignment=PP_ALIGN.CENTER)

    add_text_box(slide, 1.5, 6.0, 10, 0.5,
                 "University of East London  |  Level 4 Primers  |  Dr. Wael El Sersy",
                 font_size=14, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

    add_text_box(slide, 1.5, 6.6, 10, 0.4,
                 "April 2026",
                 font_size=12, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

    # ── Slide 2: Agenda ─────────────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 5, 0.7, "Agenda", font_size=30,
                 bold=True, color=ACCENT_BLUE)

    agenda_items = [
        "1.  Problem Introduction — What is XSS?",
        "2.  Related Work & Literature Review",
        "3.  Dataset Overview",
        "4.  Methodology & System Architecture",
        "5.  Data Preprocessing Pipeline",
        "6.  Feature Analysis",
        "7.  Model Selection & Training",
        "8.  Results & Performance Comparison",
        "9.  Live Demo",
        "10. Challenges & Solutions",
        "11. Conclusion & Future Work",
        "12. Q & A",
    ]
    add_bullet_list(slide, 1.5, 1.4, 10, 5.5, agenda_items, font_size=18)

    # ── Slide 3: Problem Introduction ───────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 8, 0.7, "What is Cross-Site Scripting (XSS)?",
                 font_size=30, bold=True, color=ACCENT_BLUE)

    items = [
        "XSS is a code injection vulnerability where attackers insert",
        "  malicious scripts into trusted web pages viewed by other users.",
        "",
        "Ranked #7 in the OWASP Top 10 (2021) critical security risks.",
        "",
        "Impact of successful XSS attacks:",
        "  • Session hijacking — stealing authentication cookies",
        "  • Data exfiltration — capturing passwords and credit cards",
        "  • Phishing — redirecting users to fraudulent sites",
        "  • Malware distribution — serving drive-by downloads",
        "",
        "Three main types: Stored, Reflected, and DOM-based XSS.",
    ]
    add_bullet_list(slide, 1.0, 1.3, 11, 5.5, items, font_size=17)

    # ── Slide 4: Why ML for XSS Detection? ──────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Why Machine Learning?",
                 font_size=30, bold=True, color=ACCENT_BLUE)

    items = [
        "Traditional WAFs use rule-based pattern matching:",
        "  ✗ High false-positive rates on JS-heavy pages",
        "  ✗ Cannot detect obfuscated or zero-day payloads",
        "  ✗ Require continuous manual signature updates",
        "",
        "Machine Learning advantages:",
        "  ✓ Learns complex, non-linear decision boundaries",
        "  ✓ Detects novel attack variants without explicit rules",
        "  ✓ Adapts to evolving attack patterns with retraining",
        "  ✓ Provides probability scores for risk assessment",
    ]
    add_bullet_list(slide, 1.0, 1.3, 11, 5.5, items, font_size=17)

    # ── Slide 5: Related Work ───────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Related Work & Literature",
                 font_size=30, bold=True, color=ACCENT_BLUE)

    items = [
        "Likarish et al. (2009) — SVM/NB on HTTP parameters → 92% acc.",
        "Wang et al. (2018) — CNN on character sequences → 99.2% acc.",
        "Mokbal et al. (2019) — MLP with 42 dynamic features → 99.0% acc.",
        "Mokbal et al. (2021) — XGBoost + IG-SBS feature selection → 99.4% acc.",
        "Fang et al. (2018) — LSTM for sequential XSS patterns → 98.2% acc.",
        "Zhou & Wang (2019) — RF ensemble with HTML/JS/URL → 98.8% acc.",
        "",
        "Our contribution: Systematic comparison of RF, XGBoost, and LR",
        "  on the same 138K-sample dataset with 66 optimally selected features.",
    ]
    add_bullet_list(slide, 1.0, 1.3, 11, 5.5, items, font_size=16)

    # ── Slide 6: Dataset Overview ───────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Dataset Overview",
                 font_size=30, bold=True, color=ACCENT_BLUE)

    items = [
        "Source: Mokbal et al. — github.com/fawaz2015/XSS-dataset",
        "Total samples: 138,567",
        "  • Normal (Benign): 99,999  (72.1%)",
        "  • XSS Attack: 38,568  (27.9%)",
        "Features: 66 pre-selected via IG-SBS from 167 original",
        "Feature categories:",
        "  • URL features (11) — URL structure and content",
        "  • HTML features (38) — DOM tags, attributes, event handlers",
        "  • JavaScript features (17) — API calls, code complexity",
        "All features are integer-valued counts.",
    ]
    add_bullet_list(slide, 1.0, 1.3, 6.5, 5.5, items, font_size=16)

    add_image_safe(slide, fig_dir / "01_class_distribution.png", 8.0, 1.5, 4.8, 4.0)

    # ── Slide 7: System Architecture ────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "System Architecture",
                 font_size=30, bold=True, color=ACCENT_BLUE)

    items = [
        "End-to-end ML pipeline:",
        "",
        "  Raw CSV  →  Preprocessing  →  Feature Scaling",
        "                                       ↓",
        "  Evaluation  ←  Training (CV)  ←  Train/Val/Test Split",
        "       ↓",
        "  Streamlit Demo App",
        "",
        "Key design decisions:",
        "  • Stratified 70/15/15 split preserving class distribution",
        "  • StandardScaler fitted on train only (no data leakage)",
        "  • 5-fold stratified cross-validation for robust estimation",
        "  • All config centralised in config.yaml",
    ]
    add_bullet_list(slide, 1.0, 1.3, 11, 5.5, items, font_size=16)

    # ── Slide 8: Preprocessing ──────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Data Preprocessing",
                 font_size=30, bold=True, color=ACCENT_BLUE)

    items = [
        "1. Load CSV with 66 named features + class label",
        "2. Remove duplicate rows",
        "3. Impute missing values with column medians",
        "4. Stratified train/validation/test split (70/15/15)",
        "5. StandardScaler normalisation (zero mean, unit variance)",
        "6. Save processed arrays + scaler to data/processed/",
        "",
        "Split sizes:",
        "  • Training: ~96,997 samples",
        "  • Validation: ~20,785 samples",
        "  • Test: ~20,785 samples",
    ]
    add_bullet_list(slide, 1.0, 1.3, 11, 5.5, items, font_size=17)

    # ── Slide 9: Feature Analysis ───────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Feature Analysis",
                 font_size=30, bold=True, color=ACCENT_BLUE)

    add_image_safe(slide, fig_dir / "02_correlation_heatmap.png", 0.5, 1.3, 6.0, 5.5)
    add_image_safe(slide, fig_dir / "03_feature_importance.png", 6.8, 1.3, 6.0, 5.5)

    # ── Slide 10: Model Selection ───────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Model Selection",
                 font_size=30, bold=True, color=ACCENT_BLUE)

    items = [
        "Random Forest (primary model):",
        "  • Ensemble of 200 decision trees",
        "  • Robust to overfitting, interpretable feature importances",
        "",
        "XGBoost (gradient boosting):",
        "  • 200 sequential boosted trees, learning rate 0.1",
        "  • Used in original XGBXSS paper — enables direct comparison",
        "",
        "Logistic Regression (baseline):",
        "  • Linear model to quantify gains from non-linear approaches",
        "  • Tests whether features are linearly separable",
        "",
        "All trained with 5-fold stratified cross-validation.",
    ]
    add_bullet_list(slide, 1.0, 1.3, 11, 5.5, items, font_size=16)

    # ── Slide 11: Results — Confusion Matrices ──────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Results — Confusion Matrices",
                 font_size=30, bold=True, color=ACCENT_BLUE)

    add_image_safe(slide, fig_dir / "04_confusion_matrix_random_forest.png",
                   0.3, 1.3, 4.1, 3.8)
    add_image_safe(slide, fig_dir / "05_confusion_matrix_xgboost.png",
                   4.6, 1.3, 4.1, 3.8)
    add_image_safe(slide, fig_dir / "06_confusion_matrix_logistic_regression.png",
                   8.9, 1.3, 4.1, 3.8)

    # ── Slide 12: Results — ROC Curves ──────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Results — ROC & PR Curves",
                 font_size=30, bold=True, color=ACCENT_BLUE)

    add_image_safe(slide, fig_dir / "06_roc_curves_comparison.png",
                   0.5, 1.3, 6.0, 5.5)
    add_image_safe(slide, fig_dir / "07_precision_recall_curves.png",
                   6.8, 1.3, 6.0, 5.5)

    # ── Slide 13: Results — Model Comparison ────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Results — Model Comparison",
                 font_size=30, bold=True, color=ACCENT_BLUE)

    add_image_safe(slide, fig_dir / "08_model_comparison.png",
                   0.5, 1.3, 6.0, 5.5)
    add_image_safe(slide, fig_dir / "09_cv_boxplots.png",
                   6.8, 1.3, 6.0, 5.5)

    # ── Slide 14: Feature Group Analysis ────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Feature Group Importance",
                 font_size=30, bold=True, color=ACCENT_BLUE)

    items = [
        "Feature groups ranked by contribution to detection:",
        "",
        "Which signal source matters most for XSS detection?",
        "  • HTML features — DOM structure and event handlers",
        "  • JavaScript features — API calls and code patterns",
        "  • URL features — URL structure and embedded payloads",
    ]
    add_bullet_list(slide, 0.8, 1.3, 5.5, 4, items, font_size=16)
    add_image_safe(slide, fig_dir / "10_feature_group_analysis.png",
                   7.0, 1.3, 5.8, 4.5)

    # ── Slide 15: Demo ──────────────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Live Demo",
                 font_size=30, bold=True, color=ACCENT_BLUE)

    items = [
        "Interactive Streamlit web application:",
        "",
        "  • Sample Predictions — 10 random test cases with labels",
        "  • Model Performance — metrics dashboard with all figures",
        "  • Manual Input — enter feature values for real-time prediction",
        "",
        "Launch command:",
        "  streamlit run demo/app.py",
        "",
        "The demo loads trained models from models/ directory",
        "and shows predictions with confidence scores.",
    ]
    add_bullet_list(slide, 1.0, 1.3, 11, 5.5, items, font_size=17)

    # ── Slide 16: Challenges & Solutions ────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Challenges & Solutions",
                 font_size=30, bold=True, color=ACCENT_BLUE)

    items = [
        "Challenge 1: Class imbalance (72% vs 28%)",
        "  → Used stratified splitting and F1-score evaluation",
        "",
        "Challenge 2: High-dimensional feature space (66 features)",
        "  → Leveraged pre-selected IG-SBS features; analysed correlations",
        "",
        "Challenge 3: Ensuring reproducibility",
        "  → Fixed random seeds, centralised config, persisted all artefacts",
        "",
        "Challenge 4: Preventing data leakage",
        "  → Scaler fitted on training set only; strict split boundaries",
    ]
    add_bullet_list(slide, 1.0, 1.3, 11, 5.5, items, font_size=16)

    # ── Slide 17: Conclusion & Future Work ──────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Conclusion & Future Work",
                 font_size=30, bold=True, color=ACCENT_BLUE)

    items = [
        "Conclusions:",
        "  • Ensemble methods (RF, XGBoost) outperform linear baseline",
        "  • Feature importance aligns with known XSS attack patterns",
        "  • 66 pre-selected features are sufficient for high-accuracy detection",
        "  • Fully reproducible pipeline: one command runs everything",
        "",
        "Future work:",
        "  • Deep learning (LSTM/Transformer) for raw payload analysis",
        "  • Real-time feature extraction from live web traffic",
        "  • Multi-class classification (Stored vs Reflected vs DOM XSS)",
        "  • Adversarial robustness testing and defence",
        "  • Integration with WAF systems (ModSecurity plugin)",
    ]
    add_bullet_list(slide, 1.0, 1.3, 11, 5.5, items, font_size=16)

    # ── Slide 18: Q&A ───────────────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)

    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(0), Inches(13.333), Inches(0.08)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT_BLUE
    shape.line.fill.background()

    add_text_box(slide, 1.5, 2.5, 10, 1.5,
                 "Questions & Answers",
                 font_size=40, bold=True, color=WHITE,
                 alignment=PP_ALIGN.CENTER)

    add_text_box(slide, 1.5, 4.2, 10, 0.6,
                 "Thank you for your attention!",
                 font_size=20, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

    add_text_box(slide, 1.5, 5.3, 10, 0.5,
                 "Team Blackhat  —  Mohammad Ibrahim · Omar Adel · Mohamed Ahmed",
                 font_size=16, color=ACCENT_BLUE, alignment=PP_ALIGN.CENTER)

    add_text_box(slide, 1.5, 5.9, 10, 0.5,
                 "University of East London  |  Level 4 Primers  |  Dr. Wael El Sersy",
                 font_size=13, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

    # ── Save ────────────────────────────────────────────────────────
    output_path = PROJECT_ROOT / "presentation" / "Blackhat_Presentation.pptx"
    prs.save(str(output_path))
    print(f"Presentation saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    create_presentation()
