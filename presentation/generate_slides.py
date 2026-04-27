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
DARK_BG = RGBColor(0x1A, 0x1A, 0x2E)
ACCENT_BLUE = RGBColor(0x00, 0xB4, 0xD8)
ACCENT_GREEN = RGBColor(0x2E, 0xCC, 0x71)
ACCENT_RED = RGBColor(0xE7, 0x4C, 0x3C)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xCC, 0xCC, 0xCC)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
def set_slide_bg(slide, color=DARK_BG):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color
def add_text_box(slide, left, top, width, height, text, font_size=18,
                 bold=False, color=WHITE, alignment=PP_ALIGN.LEFT,
                 font_name="Calibri"):
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
    if Path(img_path).exists():
        if height:
            slide.shapes.add_picture(str(img_path), Inches(left), Inches(top),
                                     Inches(width), Inches(height))
        else:
            slide.shapes.add_picture(str(img_path), Inches(left), Inches(top),
                                     Inches(width))
    else:
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
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    fig_dir = PROJECT_ROOT / "figures"
    slide = prs.slides.add_slide(prs.slide_layouts[6])  
    set_slide_bg(slide)
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(0), Inches(13.333), Inches(0.08)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT_BLUE
    shape.line.fill.background()
    add_text_box(slide, 1.5, 1.5, 10, 1.5,
                 ,
                 font_size=36, bold=True, color=WHITE,
                 alignment=PP_ALIGN.CENTER)
    add_text_box(slide, 1.5, 3.2, 10, 0.8,
                 ,
                 font_size=18, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, 1.5, 4.5, 10, 0.6,
                 ,
                 font_size=24, bold=True, color=ACCENT_BLUE,
                 alignment=PP_ALIGN.CENTER)
    add_text_box(slide, 1.5, 5.2, 10, 0.5,
                 ,
                 font_size=16, color=WHITE, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, 1.5, 6.0, 10, 0.5,
                 ,
                 font_size=14, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, 1.5, 6.6, 10, 0.4,
                 ,
                 font_size=12, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 5, 0.7, "Agenda", font_size=30,
                 bold=True, color=ACCENT_BLUE)
    agenda_items = [
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
    ]
    add_bullet_list(slide, 1.5, 1.4, 10, 5.5, agenda_items, font_size=18)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 8, 0.7, "What is Cross-Site Scripting (XSS)?",
                 font_size=30, bold=True, color=ACCENT_BLUE)
    items = [
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
    ]
    add_bullet_list(slide, 1.0, 1.3, 11, 5.5, items, font_size=17)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Why Machine Learning?",
                 font_size=30, bold=True, color=ACCENT_BLUE)
    items = [
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
    ]
    add_bullet_list(slide, 1.0, 1.3, 11, 5.5, items, font_size=17)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Related Work & Literature",
                 font_size=30, bold=True, color=ACCENT_BLUE)
    items = [
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
    ]
    add_bullet_list(slide, 1.0, 1.3, 11, 5.5, items, font_size=16)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Dataset Overview",
                 font_size=30, bold=True, color=ACCENT_BLUE)
    items = [
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
    ]
    add_bullet_list(slide, 1.0, 1.3, 6.5, 5.5, items, font_size=16)
    add_image_safe(slide, fig_dir / "01_class_distribution.png", 8.0, 1.5, 4.8, 4.0)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "System Architecture",
                 font_size=30, bold=True, color=ACCENT_BLUE)
    items = [
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
    ]
    add_bullet_list(slide, 1.0, 1.3, 11, 5.5, items, font_size=16)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Data Preprocessing",
                 font_size=30, bold=True, color=ACCENT_BLUE)
    items = [
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
    ]
    add_bullet_list(slide, 1.0, 1.3, 11, 5.5, items, font_size=17)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Feature Analysis",
                 font_size=30, bold=True, color=ACCENT_BLUE)
    add_image_safe(slide, fig_dir / "02_correlation_heatmap.png", 0.5, 1.3, 6.0, 5.5)
    add_image_safe(slide, fig_dir / "03_feature_importance.png", 6.8, 1.3, 6.0, 5.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Model Selection",
                 font_size=30, bold=True, color=ACCENT_BLUE)
    items = [
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
    ]
    add_bullet_list(slide, 1.0, 1.3, 11, 5.5, items, font_size=16)
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
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Results — ROC & PR Curves",
                 font_size=30, bold=True, color=ACCENT_BLUE)
    add_image_safe(slide, fig_dir / "06_roc_curves_comparison.png",
                   0.5, 1.3, 6.0, 5.5)
    add_image_safe(slide, fig_dir / "07_precision_recall_curves.png",
                   6.8, 1.3, 6.0, 5.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Results — Model Comparison",
                 font_size=30, bold=True, color=ACCENT_BLUE)
    add_image_safe(slide, fig_dir / "08_model_comparison.png",
                   0.5, 1.3, 6.0, 5.5)
    add_image_safe(slide, fig_dir / "09_cv_boxplots.png",
                   6.8, 1.3, 6.0, 5.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Feature Group Importance",
                 font_size=30, bold=True, color=ACCENT_BLUE)
    items = [
        ,
        ,
        ,
        ,
        ,
        ,
    ]
    add_bullet_list(slide, 0.8, 1.3, 5.5, 4, items, font_size=16)
    add_image_safe(slide, fig_dir / "10_feature_group_analysis.png",
                   7.0, 1.3, 5.8, 4.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Live Demo",
                 font_size=30, bold=True, color=ACCENT_BLUE)
    items = [
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
    ]
    add_bullet_list(slide, 1.0, 1.3, 11, 5.5, items, font_size=17)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Challenges & Solutions",
                 font_size=30, bold=True, color=ACCENT_BLUE)
    items = [
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
    ]
    add_bullet_list(slide, 1.0, 1.3, 11, 5.5, items, font_size=16)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text_box(slide, 0.8, 0.4, 10, 0.7, "Conclusion & Future Work",
                 font_size=30, bold=True, color=ACCENT_BLUE)
    items = [
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
        ,
    ]
    add_bullet_list(slide, 1.0, 1.3, 11, 5.5, items, font_size=16)
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
                 ,
                 font_size=40, bold=True, color=WHITE,
                 alignment=PP_ALIGN.CENTER)
    add_text_box(slide, 1.5, 4.2, 10, 0.6,
                 ,
                 font_size=20, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, 1.5, 5.3, 10, 0.5,
                 ,
                 font_size=16, color=ACCENT_BLUE, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, 1.5, 5.9, 10, 0.5,
                 ,
                 font_size=13, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
    output_path = PROJECT_ROOT / "presentation" / "Blackhat_Presentation.pptx"
    prs.save(str(output_path))
    print(f"Presentation saved to: {output_path}")
    return output_path
if __name__ == "__main__":
    create_presentation()
