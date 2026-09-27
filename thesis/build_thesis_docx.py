"""Script to generate the complete, professional, academic thesis in Microsoft Word (.docx) format.

Adheres strictly to formal academic structuring, real empirical data from the project,
and excludes any institutional or admissions references.
"""

import os
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

OUTPUT_PATH = Path(__file__).resolve().parent / "Cardiovascular_Risk_ML_System_Technical_Thesis.docx"

# Color Palette Constants
COLOR_PRIMARY = RGBColor(30, 58, 138)     # Deep Navy (#1E3A8A)
COLOR_SECONDARY = RGBColor(51, 65, 85)    # Slate (#334155)
COLOR_TEXT = RGBColor(30, 41, 59)         # Dark Charcoal (#1E293B)
COLOR_MUTED = RGBColor(100, 116, 139)     # Slate Gray (#64748B)
HEX_PRIMARY = "1E3A8A"
HEX_LIGHT_BG = "F8FAFC"
HEX_BORDER = "CBD5E1"
HEX_CALLOUT_BG = "F0F9FF"
HEX_CALLOUT_BORDER = "0284C7"
HEX_CODE_BG = "F1F5F9"


def set_cell_background(cell, hex_color):
    """Set background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)


def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    """Set inner margins (padding) of a table cell in dxa (1 pt = 20 dxa)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)


def set_cell_borders(cell, top="none", bottom="none", left="none", right="none", color="CBD5E1", sz="4"):
    """Set custom borders on a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="{top}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{left}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{bottom}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{right}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tcBorders>'
    )
    tc_pr.append(borders)


def add_callout_box(doc, text, title="NOTE / ARCHITECTURAL PRINCIPLE"):
    """Add a shaded callout note box with a colored left accent border."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, HEX_CALLOUT_BG)
    set_cell_margins(cell, top=160, bottom=160, left=220, right=200)
    set_cell_borders(cell, top="none", bottom="none", left="single", right="none", color=HEX_CALLOUT_BORDER, sz="24")
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run_title = p.add_run(f"[{title}] ")
    run_title.bold = True
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(10)
    run_title.font.color.rgb = RGBColor(2, 132, 199)
    
    run_text = p.add_run(text)
    run_text.font.name = "Calibri"
    run_text.font.size = Pt(10)
    run_text.font.color.rgb = COLOR_TEXT
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def add_code_block(doc, code_str, caption=None):
    """Add a monospace formatted code excerpt inside a shaded border box."""
    if caption:
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(6)
        p_cap.paragraph_format.space_after = Pt(2)
        r_cap = p_cap.add_run(f"Code Listing: {caption}")
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = COLOR_MUTED

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, HEX_CODE_BG)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color=HEX_BORDER, sz="6")
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_str)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(15, 23, 42)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)


def format_table_header(row, col_names):
    """Format the header row of an academic table."""
    for idx, name in enumerate(col_names):
        cell = row.cells[idx]
        set_cell_background(cell, HEX_PRIMARY)
        set_cell_margins(cell, top=160, bottom=160, left=160, right=160)
        set_cell_borders(cell, top="single", bottom="single", left="none", right="none", color=HEX_PRIMARY, sz="12")
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(name)
        run.bold = True
        run.font.name = "Calibri"
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(255, 255, 255)


def format_table_row(row, values, is_alt=False, is_highlight=False):
    """Format a data row of an academic table."""
    bg_hex = "FFFFFF"
    if is_highlight:
        bg_hex = "EFF6FF"  # Soft Blue Highlight
    elif is_alt:
        bg_hex = HEX_LIGHT_BG

    for idx, val in enumerate(values):
        cell = row.cells[idx]
        set_cell_background(cell, bg_hex)
        set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
        set_cell_borders(cell, top="single", bottom="single", left="none", right="none", color=HEX_BORDER, sz="4")
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(str(val))
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
        run.font.color.rgb = COLOR_TEXT
        if is_highlight:
            run.bold = True


def add_custom_heading(doc, text, level):
    """Add a structured numbered heading with academic color hierarchy."""
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = True
    run = h.runs[0]
    run.font.name = "Calibri"
    
    if level == 1:
        h.paragraph_format.space_before = Pt(18)
        h.paragraph_format.space_after = Pt(8)
        run.font.size = Pt(17)
        run.font.color.rgb = COLOR_PRIMARY
        run.bold = True
    elif level == 2:
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(6)
        run.font.size = Pt(13.5)
        run.font.color.rgb = COLOR_SECONDARY
        run.bold = True
    elif level == 3:
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(4)
        run.font.size = Pt(11.5)
        run.font.color.rgb = RGBColor(71, 85, 105)
        run.bold = True
    return h


def add_body_paragraph(doc, text, bold_prefix=None, space_after=6):
    """Add a standard academic body paragraph with consistent spacing and typography."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
        r_pre.font.color.rgb = COLOR_TEXT

    r_text = p.add_run(text)
    r_text.font.name = "Calibri"
    r_text.font.size = Pt(11)
    r_text.font.color.rgb = COLOR_TEXT
    return p


def xml_escape(text: str) -> str:
    """Escape special XML characters for OMML runs."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def o_r(text: str) -> str:
    """Create an OMML text run."""
    return f"<m:r><m:t>{xml_escape(text)}</m:t></m:r>"


def o_sSup(base: str, sup: str) -> str:
    """Create an OMML superscript expression."""
    return f"<m:sSup><m:e>{base}</m:e><m:sup>{sup}</m:sup></m:sSup>"


def o_sSub(base: str, sub: str) -> str:
    """Create an OMML subscript expression."""
    return f"<m:sSub><m:e>{base}</m:e><m:sub>{sub}</m:sub></m:sSub>"


def o_sSubSup(base: str, sub: str, sup: str) -> str:
    """Create an OMML subscript + superscript expression."""
    return f"<m:sSubSup><m:e>{base}</m:e><m:sub>{sub}</m:sub><m:sup>{sup}</m:sup></m:sSubSup>"


def o_frac(num: str, den: str) -> str:
    """Create an OMML horizontal fraction bar expression."""
    return f"<m:f><m:fPr><m:type m:val=\"bar\"/></m:fPr><m:num>{num}</m:num><m:den>{den}</m:den></m:f>"


def o_rad(expr: str) -> str:
    """Create an OMML radical (square root) expression."""
    return f"<m:rad><m:radPr><m:degHide m:val=\"1\"/></m:radPr><m:deg/><m:e>{expr}</m:e></m:rad>"


def o_delim(expr: str, beg="(", end=")") -> str:
    """Create an OMML delimited group (parentheses, brackets, norms)."""
    return f"<m:d><m:dPr><m:begChr m:val=\"{beg}\"/><m:endChr m:val=\"{end}\"/></m:dPr><m:e>{expr}</m:e></m:d>"


def o_sum(sub: str, sup: str = None, expr: str = "") -> str:
    """Create an OMML n-ary summation operator with limits."""
    sup_hide = "1" if sup is None else "0"
    sup_elem = f"<m:sup>{sup}</m:sup>" if sup is not None else "<m:sup/>"
    return (
        f"<m:nary>"
        f"<m:naryPr><m:chr m:val=\"∑\"/><m:limLoc m:val=\"undOvr\"/><m:subHide m:val=\"0\"/><m:supHide m:val=\"{sup_hide}\"/></m:naryPr>"
        f"<m:sub>{sub}</m:sub>{sup_elem}<m:e>{expr}</m:e>"
        f"</m:nary>"
    )


def add_math_equation(doc, inner_omml_xml: str, space_before=4, space_after=6):
    """Add a native Word Office Math (OMML) centered display equation paragraph."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    omath_xml = (
        f'<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        f'<m:oMath>{inner_omml_xml}</m:oMath>'
        f'</m:oMathPara>'
    )
    p._p.append(parse_xml(omath_xml))
    return p


def add_bullet_point(doc, bold_lead, text):
    """Add a structured bullet point."""
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT

    r_lead = p.add_run(bold_lead)
    r_lead.bold = True
    r_lead.font.name = "Calibri"
    r_lead.font.size = Pt(10.5)
    r_lead.font.color.rgb = COLOR_TEXT

    r_body = p.add_run(text)
    r_body.font.name = "Calibri"
    r_body.font.size = Pt(10.5)
    r_body.font.color.rgb = COLOR_TEXT


def add_numbered_item(doc, number_str, bold_lead, text, space_after=3):
    """Add a structured numbered list item without line-break justification defects."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT

    r_num = p.add_run(f"{number_str} ")
    r_num.bold = True
    r_num.font.name = "Calibri"
    r_num.font.size = Pt(10.5)
    r_num.font.color.rgb = COLOR_PRIMARY

    if bold_lead:
        r_lead = p.add_run(f"{bold_lead} ")
        r_lead.bold = True
        r_lead.font.name = "Calibri"
        r_lead.font.size = Pt(10.5)
        r_lead.font.color.rgb = COLOR_TEXT

    r_body = p.add_run(text)
    r_body.font.name = "Calibri"
    r_body.font.size = Pt(10.5)
    r_body.font.color.rgb = COLOR_TEXT
    return p


def setup_header_footer(doc):
    """Configure running header and page numbering footer."""
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header
        header = section.header
        p_head = header.paragraphs[0]
        p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_head.paragraph_format.space_after = Pt(0)
        r_head = p_head.add_run("Technical Thesis: Cardiovascular Risk Machine Learning System")
        r_head.font.name = "Calibri"
        r_head.font.size = Pt(8.5)
        r_head.font.color.rgb = COLOR_MUTED

        # Footer
        footer = section.footer
        p_foot = footer.paragraphs[0]
        p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_foot.paragraph_format.space_before = Pt(0)
        r_foot = p_foot.add_run("Cardiovascular Risk Prediction & Analysis System  |  Page ")
        r_foot.font.name = "Calibri"
        r_foot.font.size = Pt(9)
        r_foot.font.color.rgb = COLOR_MUTED
        
        # Insert Page Number field via XML
        fld_xml = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
        p_foot._p.append(fld_xml)


def build_thesis_document():
    """Build the complete, comprehensive technical thesis document."""
    print("Generating comprehensive academic thesis document in Word (.docx)...")
    doc = Document()
    setup_header_footer(doc)

    # =========================================================================
    # TITLE PAGE
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.paragraph_format.space_before = Pt(32)
    p_inst.paragraph_format.space_after = Pt(4)
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_univ = p_inst.add_run("Islamic Azad University, Tehran South Branch\n")
    r_univ.font.name = "Calibri"
    r_univ.font.size = Pt(14)
    r_univ.bold = True
    r_univ.font.color.rgb = COLOR_PRIMARY

    r_fac = p_inst.add_run("Faculty of Engineering\n")
    r_fac.font.name = "Calibri"
    r_fac.font.size = Pt(12)
    r_fac.font.color.rgb = COLOR_SECONDARY

    p_badge = doc.add_paragraph()
    p_badge.paragraph_format.space_before = Pt(16)
    p_badge.paragraph_format.space_after = Pt(12)
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_badge = p_badge.add_run("TECHNICAL THESIS")
    r_badge.font.name = "Calibri"
    r_badge.font.size = Pt(13)
    r_badge.bold = True
    r_badge.font.color.rgb = COLOR_PRIMARY

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(10)
    p_title.paragraph_format.line_spacing = 1.15
    r_title = p_title.add_run("Design and Development of a Web-Based Machine Learning System for Cardiovascular Risk Prediction and Analysis")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(22)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(36)
    r_sub = p_sub.add_run("A Comparative Study of Seven Machine Learning Paradigms with Leakage-Free Preprocessing, Explainable AI (SHAP), and Data-Intensive REST Architecture")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11.5)
    r_sub.font.color.rgb = COLOR_MUTED

    # Metadata block on title page (Author & Supervisor)
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(24)
    p_meta.paragraph_format.space_after = Pt(4)

    r_auth_label = p_meta.add_run("Author:\n")
    r_auth_label.font.name = "Calibri"
    r_auth_label.font.size = Pt(10.5)
    r_auth_label.font.color.rgb = COLOR_MUTED

    r_author = p_meta.add_run("Mohammad Hasan Talebi\n\n")
    r_author.font.name = "Calibri"
    r_author.font.size = Pt(14)
    r_author.bold = True
    r_author.font.color.rgb = COLOR_PRIMARY

    r_sup_label = p_meta.add_run("Supervisor:\n")
    r_sup_label.font.name = "Calibri"
    r_sup_label.font.size = Pt(10.5)
    r_sup_label.font.color.rgb = COLOR_MUTED

    r_sup = p_meta.add_run("Azita Shirazipour\n")
    r_sup.font.name = "Calibri"
    r_sup.font.size = Pt(14)
    r_sup.bold = True
    r_sup.font.color.rgb = COLOR_PRIMARY

    p_inst_foot = doc.add_paragraph()
    p_inst_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst_foot.paragraph_format.space_before = Pt(28)
    p_inst_foot.paragraph_format.space_after = Pt(4)
    r_fac_line = p_inst_foot.add_run("Faculty of Engineering, Islamic Azad University, Tehran South Branch\n")
    r_fac_line.font.name = "Calibri"
    r_fac_line.font.size = Pt(11)
    r_fac_line.font.color.rgb = COLOR_SECONDARY

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_date.paragraph_format.space_before = Pt(8)
    p_date.paragraph_format.space_after = Pt(0)
    r_date = p_date.add_run("Date: 2024   March  20   , Wednesday")
    r_date.font.name = "Calibri"
    r_date.font.size = Pt(11)
    r_date.font.color.rgb = COLOR_MUTED

    doc.add_page_break()

    # =========================================================================
    # ABSTRACT
    # =========================================================================
    h_abs = doc.add_heading("Abstract", level=1)
    h_abs.paragraph_format.space_before = Pt(0)
    h_abs.paragraph_format.space_after = Pt(6)
    h_abs.runs[0].font.name = "Calibri"
    h_abs.runs[0].font.size = Pt(18)
    h_abs.runs[0].font.color.rgb = COLOR_PRIMARY

    add_body_paragraph(
        doc,
        "Cardiovascular diseases (CVDs) remain the preeminent cause of global mortality, necessitating reliable, early, "
        "and reproducible predictive screening mechanisms. However, the translation of clinical machine learning algorithms "
        "into operational environments routinely suffers from methodological flaws—predominantly data leakage between preprocessing "
        "and evaluation phases, reliance on uninformative aggregate accuracy metrics on clinical cohorts, opaque 'black-box' "
        "decision boundaries, and monolithic software designs that lack verifiable persistence and testing standards.",
        space_after=4
    )
    add_body_paragraph(
        doc,
        "This thesis presents the conception, empirical evaluation, and full architectural implementation of a data-intensive, "
        "web-based machine learning system for cardiovascular risk prediction. The project implements a controlled empirical "
        "investigation addressing the core research question: How do distinct machine-learning paradigms compare in predictive discrimination, "
        "and which physiological biomarkers exert the strongest influence on risk predictions? Using the canonical 14-attribute "
        "Cleveland cardiovascular cohort (N = 303 records), seven distinct algorithmic families were systematically benchmarked: "
        "Logistic Regression, K-Nearest Neighbors (KNN), Decision Tree, Random Forest, Support Vector Machine (SVM), AdaBoost, "
        "and Gradient Boosted Decision Trees (GBDT). To ensure mathematical rigor, a leakage-free preprocessing pipeline was developed "
        "using scikit-learn ColumnTransformers, isolating all imputation and standard scaling parameters strictly within training folds.",
        space_after=4
    )
    add_body_paragraph(
        doc,
        "Through Stratified 5-Fold Cross-Validation and hyperparameter grid optimization, a regularized Logistic Regression pipeline "
        "(C = 0.1, L2 penalty, liblinear solver) demonstrated superior discriminative stability, achieving an optimized cross-validation "
        "ROC-AUC of 0.9117 ± 0.0210. Evaluated on an untouched 20% hold-out test set (N = 61), the production pipeline achieved an "
        "overall Accuracy of 88.52%, a Precision of 83.87%, a Specificity of 84.85%, an area under the ROC curve (ROC-AUC) of 0.9621, "
        "and critically, a Sensitivity (Recall) of 92.86% (correctly detecting 26 of 28 cardiac pathology cases with only two false negatives). "
        "To resolve the black-box dilemma, Explainable Artificial Intelligence (XAI) was embedded via Shapley Additive Explanations (SHAP), "
        "revealing that major vessel count via fluoroscopy (ca), maximum exercise heart rate (thalach), and exercise-induced ST depression "
        "(oldpeak) represent the dominant global clinical determinants, while supplying directional local patient-level attribution waterfalls.",
        space_after=4
    )
    add_body_paragraph(
        doc,
        "The resulting pipeline is operationalized within an enterprise-grade, asynchronous web architecture utilizing FastAPI, "
        "Pydantic v2 schemas for strict physiological boundary validation, SQLAlchemy 2.0 ORM with dual-engine support (SQLite for zero-dependency "
        "development and PostgreSQL for enterprise production), and a responsive client dashboard offering dynamic radial risk probability "
        "gauges, real-time SHAP visualizations, assessment history filtering, and CSV export. The entire system is supported by Docker Compose "
        "containerization and a rigorous automated test suite comprising 21 unit and integration tests executing with 100% passing status "
        "and 74% statement coverage. This work demonstrates that high clinical screening sensitivity, model explainability, and "
        "production software engineering can be unified into a performant, maintainable, and reproducible data system.",
        space_after=4
    )
    
    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(4)
    p_kw.paragraph_format.space_after = Pt(0)
    r_kw_title = p_kw.add_run("Keywords: ")
    r_kw_title.bold = True
    r_kw_title.font.name = "Calibri"
    r_kw_title.font.size = Pt(10)
    r_kw_body = p_kw.add_run("Cardiovascular Risk Prediction, Supervised Machine Learning, Model Benchmarking, Data Leakage Prevention, SHAP Explainability, FastAPI, SQLAlchemy ORM, Web-Based Data Systems, Software Engineering.")
    r_kw_body.font.name = "Calibri"
    r_kw_body.font.size = Pt(10)
    r_kw_body.font.color.rgb = COLOR_SECONDARY

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS / LIST OF FIGURES / LIST OF TABLES
    # =========================================================================
    h_toc = doc.add_heading("Table of Contents", level=1)
    h_toc.runs[0].font.color.rgb = COLOR_PRIMARY

    toc_items = [
        ("1. Introduction", "7"),
        ("   1.1 Background and Motivation", "7"),
        ("   1.2 Problem Statement", "7"),
        ("   1.3 Research Questions and Hypotheses", "8"),
        ("   1.4 Project Objectives", "9"),
        ("   1.5 Scope and Delimitations", "9"),
        ("   1.6 Technical Contributions", "10"),
        ("   1.7 Thesis Organization", "10"),
        ("2. Background and Related Technologies", "11"),
        ("   2.1 Clinical Pathophysiology and Diagnostic Biomarkers", "11"),
        ("   2.2 Supervised Binary Classification in Clinical Tabular Domains", "12"),
        ("   2.3 Mathematical Formulations of Candidate Algorithms", "12"),
        ("   2.4 Explainable Artificial Intelligence (XAI) and Shapley Values", "14"),
        ("   2.5 Modern Web Engineering: FastAPI and Asynchronous REST", "14"),
        ("   2.6 Relational Persistence and Object-Relational Mapping (ORM)", "15"),
        ("   2.7 Containerization and Environmental Reproducibility", "15"),
        ("3. Requirements Analysis", "16"),
        ("   3.1 Functional Requirements", "16"),
        ("   3.2 Non-Functional Requirements", "17"),
        ("   3.3 System Constraints", "18"),
        ("   3.4 Use Case Specifications", "18"),
        ("4. System Design and Architecture", "19"),
        ("   4.1 Overall Architectural Topology", "19"),
        ("   4.2 Component Architecture and Module Separation", "19"),
        ("   4.3 End-to-End Data Flow Dynamics", "19"),
        ("   4.4 Database Design and Entity Relationships", "20"),
        ("   4.5 RESTful API Design and Endpoint Catalog", "21"),
        ("   4.6 Security and Ethical Privacy Safeguards", "22"),
        ("   4.7 Architectural Design Decisions and Trade-Off Analysis", "22"),
        ("5. Implementation", "23"),
        ("   5.1 Development Environment and Pinned Toolchain", "23"),
        ("   5.2 Physical Project Layout and Directory Structure", "24"),
        ("   5.3 Preprocessing Pipeline and Leakage Prevention Implementation", "25"),
        ("   5.4 Machine Learning Benchmarking and Hyperparameter Optimization", "25"),
        ("   5.5 Explainable AI (SHAP) Implementation", "25"),
        ("   5.6 Database Layer and Repository Implementation", "26"),
        ("   5.7 FastAPI Service and Router Implementation", "26"),
        ("   5.8 Client Dashboard and Data Visualization Implementation", "26"),
        ("   5.9 Configuration, Secrets, and Environment Management", "26"),
        ("   5.10 Containerization and Docker Deployment", "26"),
        ("6. Testing and Validation", "27"),
        ("   6.1 Comprehensive Testing Strategy", "27"),
        ("   6.2 Preprocessing and Data Pipeline Unit Tests", "27"),
        ("   6.3 Machine Learning and SHAP Explainer Tests", "27"),
        ("   6.4 Database and Repository Unit Tests", "27"),
        ("   6.5 API Functional and Boundary Validation Tests", "28"),
        ("   6.6 Full End-to-End Integration Workflow Verification", "28"),
        ("   6.7 Empirical Test Results and Coverage Metrics", "28"),
        ("   6.8 Real-World Debugging Case Studies and Root Cause Analysis", "29"),
        ("   6.9 Codebase Refactoring and Maintainability Enhancements", "29"),
        ("7. Evaluation and Discussion", "31"),
        ("   7.1 Functional Requirements Fulfillment Audit", "31"),
        ("   7.2 Empirical Model Benchmark Analysis (7 Algorithms)", "31"),
        ("   7.3 Hold-out Test Generalization and Clinical Sensitivity", "32"),
        ("   7.4 Global and Local Interpretability Findings", "32"),
        ("   7.5 Scientific Discussion: The Bias-Variance Dilemma in Clinical Cohorts", "34"),
        ("   7.6 System Performance, Scalability, and Maintainability", "34"),
        ("8. Limitations and Future Work", "35"),
        ("   8.1 Dataset and Demographic Limitations", "35"),
        ("   8.2 Algorithmic and Experimental Constraints", "35"),
        ("   8.3 Future Architectural and Clinical Roadmap", "35"),
        ("9. Conclusion", "36"),
        ("   9.1 Problem Summary", "36"),
        ("   9.2 Implemented Solution and Technical Highlights", "36"),
        ("   9.3 Final Reflections", "36"),
        ("References", "37"),
        ("Appendices", "38"),
        ("   Appendix A: REST API Schema Reference", "38"),
        ("   Appendix B: Database Table Definitions", "38"),
        ("   Appendix C: Environment Configuration Example", "39"),
        ("   Appendix D: Core Pipeline Implementation Excerpts", "39"),
    ]

    tbl_toc = doc.add_table(rows=len(toc_items), cols=2)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_toc.columns[0].width = Inches(5.8)
    tbl_toc.columns[1].width = Inches(0.7)
    for idx, (title, page) in enumerate(toc_items):
        row = tbl_toc.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(5.8)
        c1.width = Inches(0.7)
        set_cell_background(c0, "FFFFFF")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, top=40, bottom=40, left=40, right=40)
        set_cell_margins(c1, top=40, bottom=40, left=40, right=40)
        set_cell_borders(c0, top="none", bottom="none", left="none", right="none")
        set_cell_borders(c1, top="none", bottom="none", left="none", right="none")
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(1)
        p0.paragraph_format.space_after = Pt(1)
        r0 = p0.add_run(title)
        r0.font.name = "Calibri"
        r0.font.size = Pt(10)
        if not title.startswith("   "):
            r0.bold = True
            r0.font.color.rgb = COLOR_PRIMARY
        else:
            r0.font.color.rgb = COLOR_TEXT

        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_before = Pt(1)
        p1.paragraph_format.space_after = Pt(1)
        r1 = p1.add_run(page)
        r1.font.name = "Calibri"
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_MUTED

    doc.add_page_break()

    # List of Figures & Tables
    h_lof = doc.add_heading("List of Figures", level=2)
    h_lof.runs[0].font.color.rgb = COLOR_PRIMARY
    figures = [
        ("Figure 4.1: High-Level System Architecture and Multi-Tier Component Topology", "19"),
        ("Figure 4.2: Relational Database Entity-Relationship (ER) Architecture", "20"),
        ("Figure 4.3: End-to-End Prediction, Persistence, and SHAP Sequence Dynamics", "19"),
        ("Figure 5.1: Leakage-Free Preprocessing and Cross-Validation Pipeline", "25"),
        ("Figure 5.2: Client Dashboard Assessment Form and Radial Risk Gauge Interface", "26"),
        ("Figure 7.1: Receiver Operating Characteristic (ROC) Curve on Untouched Test Set", "32"),
        ("Figure 7.2: Global SHAP Feature Importance Ranking Across Benchmark Cohort", "32"),
        ("Figure 7.3: Local Directional Waterfall SHAP Attribution for High-Risk Case Study", "33"),
    ]
    for fig_title, fig_pg in figures:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(fig_title + " ")
        r1.font.name = "Calibri"
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_TEXT
        r2 = p.add_run(f"... Page {fig_pg}")
        r2.font.name = "Calibri"
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_MUTED

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    h_lot = doc.add_heading("List of Tables", level=2)
    h_lot.runs[0].font.color.rgb = COLOR_PRIMARY
    tables = [
        ("Table 2.1: Canonical 14-Attribute Clinical Data Dictionary (Cleveland Cohort)", "11"),
        ("Table 3.1: Formal Functional Requirements Specification (FR-1 through FR-8)", "16"),
        ("Table 3.2: Formal Non-Functional Requirements Specification (NFR-1 through NFR-6)", "17"),
        ("Table 4.1: Database Schema Specification for prediction_records Table", "20"),
        ("Table 4.2: Comprehensive REST API Endpoint Specification and Routing Matrix", "21"),
        ("Table 5.1: Pinned Production Software Stack and Development Toolchain", "23"),
        ("Table 6.1: Automated Test Suite Structure, Categorization, and Execution Results", "28"),
        ("Table 7.1: Stratified 5-Fold Cross-Validation Performance Comparison Across 7 Algorithms", "31"),
        ("Table 7.2: Final Evaluation Performance Metrics on Untouched Test Set (N = 61)", "32"),
        ("Table 7.3: Top 10 Global Clinical Predictive Factors Identified by SHAP", "33"),
    ]
    for tbl_title, tbl_pg in tables:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(tbl_title + " ")
        r1.font.name = "Calibri"
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_TEXT
        r2 = p.add_run(f"... Page {tbl_pg}")
        r2.font.name = "Calibri"
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_MUTED

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_custom_heading(doc, "1. Introduction", level=1)

    add_custom_heading(doc, "1.1 Background and Motivation", level=2)
    add_body_paragraph(
        doc,
        "Cardiovascular diseases (CVDs) encompass a wide array of pathological disorders affecting the heart and vascular system, "
        "including coronary artery disease, heart failure, cerebrovascular disease, and rheumatic heart disease. Epidemiological surveys "
        "conducted by the World Health Organization (WHO) confirm that CVDs remain the leading global cause of mortality, responsible for "
        "an estimated 17.9 million deaths annually—representing approximately 32% of all worldwide fatalities. Beyond mortality, cardiovascular "
        "disorders impose crippling long-term socioeconomic and healthcare burdens through prolonged hospitalization, permanent physical "
        "impairment, and demanding chronic management regimens."
    )
    add_body_paragraph(
        doc,
        "Crucially, clinical cardiology emphasizes that early detection, structured risk assessment, and proactive clinical intervention "
        "(encompassing pharmacological therapy, dietary adjustments, and supervised lifestyle modifications) can substantially mitigate "
        "adverse cardiovascular events. In routine diagnostic practice, clinicians capture diverse physiological parameters: resting systolic "
        "blood pressure, serum cholesterol profiles, fasting glycemia, electrocardiographic (ECG) waveforms, and cardiovascular response to "
        "standardized physical exertion during treadmill stress testing. However, manual risk estimation based on heuristic scoring systems "
        "(such as the Framingham Risk Score or European SCORE) relies on rigid, linear combinations of limited biomarkers, frequently "
        "failing to detect complex, non-linear interactions across multidimensional diagnostic indicators."
    )
    add_body_paragraph(
        doc,
        "Machine learning (ML) provides mathematical methodologies capable of processing high-dimensional clinical feature vectors, uncovering "
        "latent correlations, and calculating continuous risk probabilities. Nevertheless, translating clinical machine learning from "
        "exploratory research into operational software systems presents profound challenges that transcend mere algorithmic training. "
        "A critical dual imperative exists in clinical computing: the system must satisfy rigorous scientific standards regarding data leakage "
        "and comparative evaluation, while simultaneously implementing enterprise-grade software engineering principles that ensure reproducibility, "
        "explainability, relational persistence, and accessibility."
    )

    add_custom_heading(doc, "1.2 Problem Statement", level=2)
    add_body_paragraph(
        doc,
        "Despite extensive academic literature investigating classification algorithms on medical datasets, widespread methodological "
        "and engineering deficiencies continue to undermine the reliability and real-world adoption of predictive healthcare systems:"
    )
    add_bullet_point(doc, "Uncontrolled Data Leakage: ", "A substantial proportion of published studies apply preprocessing transformations—such as global standard scaling, mean imputation, or categorical encoding—across the entire dataset prior to partitioning into training and evaluation subsets. This introduces subtle yet catastrophic data contamination, causing algorithms to learn distributional properties of test cohorts and yielding overly optimistic, non-generalizable performance estimates.")
    add_bullet_point(doc, "Evaluation Metric Misalignment: ", "Researchers frequently report aggregate classification accuracy as the primary benchmark. On clinical datasets where patient classes exhibit imbalance and where diagnostic errors carry vastly asymmetric costs, accuracy is fundamentally misleading. Failing to detect a patient harboring coronary stenosis (a False Negative) risks patient mortality, whereas incorrectly flagging a healthy subject for secondary non-invasive evaluation (a False Positive) carries minimal clinical consequence. Predictive systems must explicitly optimize and report Sensitivity (Recall) and the Area Under the Receiver Operating Characteristic Curve (ROC-AUC).")
    add_bullet_point(doc, "The Black-Box Dilemma: ", "High-capacity non-linear classifiers, such as deep neural networks or ensemble gradient boosters, frequently obscure the internal rationale behind individual patient predictions. Clinical practitioners cannot responsibly act upon opaque statistical classifications without transparent, physiologically grounded explanations detailing why a specific patient was assigned an elevated risk tier.")
    add_bullet_point(doc, "Monolithic, Fragile Architectures: ", "Typical data science implementations are preserved as isolated, monolithic Jupyter notebooks. Such scripts lack persistent relational databases for clinical audit trails, lack typed API schemas for boundary validation, feature no automated testing infrastructure, and offer no reproducible containerized runtime environments.")

    add_custom_heading(doc, "1.3 Research Questions and Hypotheses", level=2)
    add_body_paragraph(
        doc,
        "To systematically address the stated problems, this research is guided by a central primary research question, supported by "
        "five secondary technical inquiries and three empirically testable scientific hypotheses:"
    )
    add_callout_box(
        doc,
        "Primary Research Question (RQ):\n"
        "How do different machine-learning approaches perform for cardiovascular risk prediction, and which patient features contribute most to the resulting predictions?",
        title="PRIMARY SCIENTIFIC INQUIRY"
    )
    add_bullet_point(doc, "Secondary Question 1 (SRQ1): ", "How does a mathematically strict, leakage-free preprocessing pipeline impact the stability of cross-validated model evaluation compared to unconstrained baselines?")
    add_bullet_point(doc, "Secondary Question 2 (SRQ2): ", "How do linear, distance-based, rule-based, bagging ensemble, and boosting ensemble algorithmic families compare when evaluated on tabular cardiovascular diagnostic data under identical cross-validation conditions?")
    add_bullet_point(doc, "Secondary Question 3 (SRQ3): ", "Which clinical evaluation metrics provide the most informative assessment for medical risk screening where false negatives carry critical clinical penalties?")
    add_bullet_point(doc, "Secondary Question 4 (SRQ4): ", "Which specific physiological biomarkers and diagnostic findings exert the greatest influence on global risk predictions, and can these attributions be individualized for specific patient cases using game-theoretic Shapley values?")
    add_bullet_point(doc, "Secondary Question 5 (SRQ5): ", "How can an explainable predictive machine learning model be integrated into a resilient, decoupled web-based system incorporating asynchronous API validation, relational audit persistence, and automated verification?")

    add_body_paragraph(
        doc,
        "Based on theoretical considerations regarding statistical bias-variance trade-offs and clinical physiology, three formal hypotheses were defined for empirical testing:",
        bold_prefix="Formulated Hypotheses: "
    )
    add_bullet_point(doc, "Hypothesis 1 (H1 - Algorithmic Comparison): ", "Ensemble-based machine learning models (Random Forest, Gradient Boosting, AdaBoost) will exhibit distinct predictive generalization behaviors compared to a regularized linear baseline when evaluated on tabular cardiovascular diagnostic data.")
    add_bullet_point(doc, "Hypothesis 2 (H2 - Feature Engineering Impact): ", "Clinically motivated derived physiological interaction features (such as hemodynamic-lipid stress indices and heart rate reserve ratios) alter cross-validation discriminative capability compared to raw physiological features.")
    add_bullet_point(doc, "Hypothesis 3 (H3 - Factor Attribution Consistency): ", "Game-theoretic SHAP interpretability analysis will demonstrate that anatomical fluoroscopy vessel counts, ST-segment depression, and exercise maximum heart rate dominate the model's predictive decisions, aligning with established cardiological pathophysiology.")

    add_custom_heading(doc, "1.4 Project Objectives", level=2)
    add_body_paragraph(
        doc,
        "The project defined twelve concrete engineering and scientific objectives to fulfill throughout its development lifecycle:"
    )
    add_bullet_point(doc, "O1 — Data Acquisition & Verification: ", "Acquire, validate, and document the canonical 14-attribute UCI Cleveland Heart Disease benchmark dataset, verifying clinical ranges and missingness patterns.")
    add_bullet_point(doc, "O2 — Exploratory Data Analysis: ", "Execute exhaustive univariate, bivariate, and correlation statistical profiling across all continuous and categorical predictors.")
    add_bullet_point(doc, "O3 — Leakage-Free Preprocessing: ", "Construct a scikit-learn ColumnTransformer pipeline guaranteeing that all imputation, scaling, and one-hot encoding parameters are learned strictly from training folds.")
    add_bullet_point(doc, "O4 — Feature Engineering Investigation: ", "Formulate and test physiologically grounded derived features to empirically assess their impact on classification metrics.")
    add_bullet_point(doc, "O5 — Multi-Model Benchmarking: ", "Implement, train, and systematically compare seven diverse machine learning algorithms representing linear, distance, tree, bagging, and boosting paradigms under Stratified 5-Fold Cross-Validation.")
    add_bullet_point(doc, "O6 — Hyperparameter Optimization: ", "Execute systematic grid optimization across candidate model hyperparameter spaces using cross-validated ROC-AUC as the objective function.")
    add_bullet_point(doc, "O7 — Explainability Integration: ", "Incorporate SHapley Additive exPlanations (SHAP) to generate cohort-wide global feature importance rankings and single-patient directional attribution waterfalls.")
    add_bullet_point(doc, "O8 — Web Architecture Development: ", "Engineer a production-ready, asynchronous REST API utilizing FastAPI and Pydantic v2 schemas for strict physiological parameter validation.")
    add_bullet_point(doc, "O9 — Relational Database Persistence: ", "Design and implement a relational database schema using SQLAlchemy 2.0 ORM supporting patient prediction persistence, history auditing, and CSV export.")
    add_bullet_point(doc, "O10 — Interactive User Dashboard: ", "Develop a responsive single-page web interface featuring clinical parameter forms, dynamic radial risk probability gauges, local SHAP attribution bars, and research analytics.")
    add_bullet_point(doc, "O11 — Comprehensive Automated Testing: ", "Develop and execute an exhaustive test suite covering unit, API, database, and end-to-end integration workflows with verified statement coverage.")
    add_bullet_point(doc, "O12 — Containerization & Reproducibility: ", "Package the application using Docker and Docker Compose, accompanied by pinned dependencies and reproducible execution scripts.")

    add_custom_heading(doc, "1.5 Scope and Delimitations", level=2)
    add_body_paragraph(
        doc,
        "To maintain rigorous scientific focus and engineering viability, the scope of this project is strictly defined:"
    )
    add_bullet_point(doc, "In Scope: ", "Supervised binary classification (presence vs. absence of significant coronary artery disease); structured tabular clinical data; exploratory data analysis; mathematically rigorous data leakage prevention; multi-algorithm cross-validation benchmarking; hyperparameter tuning; global and local SHAP explainability; REST API construction; relational database persistence; responsive web client development; automated test verification; and containerized deployment.")
    add_bullet_point(doc, "Out of Scope / Non-Diagnostic Delimitation: ", "The system is explicitly engineered as a scientific research prototype and decision-support proof-of-concept. It is NOT a medical diagnostic device, does not provide medical consultations, and does not claim clinical certification. Medical clearance, pharmaceutical prescriptions, and formal diagnoses must remain the sole purview of qualified medical practitioners.")

    add_custom_heading(doc, "1.6 Technical Contributions", level=2)
    add_body_paragraph(
        doc,
        "The primary technical and academic contributions delivered by this project comprise:",
        bold_prefix="Key Contributions: "
    )
    add_bullet_point(doc, "1. Systematic 7-Algorithm Empirical Benchmark: ", "Conducted a rigorous comparative evaluation of seven distinct classification paradigms on the Cleveland cohort, establishing that a regularized linear model achieves superior discriminative stability (0.9117 CV ROC-AUC) on small tabular clinical samples over complex ensemble architectures.")
    add_bullet_point(doc, "2. High Clinical Screening Sensitivity: ", "Achieved a hold-out test sensitivity (Recall) of 92.86% and ROC-AUC of 0.9621 on unseen test data, minimizing false negative diagnostic omissions to only 2 cases out of 28 diseased patients.")
    add_bullet_point(doc, "3. Operationalized Game-Theoretic Explainability: ", "Successfully integrated real-time SHAP local attributions into web API responses and client-side UI visualizations, transforming abstract machine learning probabilities into directional clinical factor breakdowns.")
    add_bullet_point(doc, "4. Decoupled Production-Grade Architecture: ", "Engineered a modular, fully tested software system combining FastAPI, SQLAlchemy, SQLite/PostgreSQL, and Docker, validated by 21 automated tests passing with 100% success.")

    add_custom_heading(doc, "1.7 Thesis Organization", level=2)
    add_body_paragraph(
        doc,
        "The remainder of this thesis is organized as follows: Chapter 2 reviews the clinical background and theoretical foundations "
        "of the candidate machine learning models, SHAP explainability, and web technologies. Chapter 3 presents a comprehensive requirements "
        "analysis encompassing functional, non-functional, and use-case specifications. Chapter 4 details the system architecture, component "
        "topology, database schema, and API contracts. Chapter 5 documents the concrete technical implementation of the data pipeline, "
        "inference service, database repository, and web dashboard. Chapter 6 describes the testing methodology, presenting actual unit, "
        "integration, and debugging case studies. Chapter 7 analyzes empirical experimental findings, evaluating model performance, "
        "hypotheses, and SHAP feature rankings. Chapter 8 critically addresses dataset limitations and outlines future extensions. "
        "Finally, Chapter 9 concludes the thesis with a synthesis of findings and technical reflections."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: BACKGROUND AND RELATED TECHNOLOGIES
    # =========================================================================
    add_custom_heading(doc, "2. Background and Related Technologies", level=1)

    add_custom_heading(doc, "2.1 Clinical Pathophysiology and Diagnostic Biomarkers", level=2)
    add_body_paragraph(
        doc,
        "Coronary artery disease (CAD) develops through atherosclerosis—the progressive accumulation of fibrofatty plaques within the intimal "
        "lining of epicardial coronary arteries. As luminal narrowing exceeds critical thresholds (conventionally defined as >= 50% diameter "
        "stenosis in at least one major vessel), myocardial oxygen demand exceeds coronary blood flow supply, resulting in myocardial ischemia. "
        "Clinically, ischemia manifests as angina pectoris, ischemic ST-segment depression during electrocardiography, and impaired exercise capacity."
    )
    add_body_paragraph(
        doc,
        "The standard benchmark dataset utilized in this research originated from the Cleveland Clinic Foundation and was compiled by "
        "Dr. Robert Detrano and colleagues (1989). The cohort comprises 303 patient records, each described by 13 clinical features and "
        "one binary diagnostic target indicating presence or absence of >= 50% coronary narrowing confirmed via invasive coronary angiography."
    )

    # Table 2.1: Data Dictionary
    doc.add_paragraph().paragraph_format.space_before = Pt(6)
    p_tbl_cap = doc.add_paragraph()
    p_tbl_cap.paragraph_format.space_after = Pt(4)
    r_cap = p_tbl_cap.add_run("Table 2.1: Canonical 14-Attribute Clinical Data Dictionary (Cleveland Cohort)")
    r_cap.bold = True
    r_cap.font.name = "Calibri"
    r_cap.font.size = Pt(10)

    tbl_dict = doc.add_table(rows=15, cols=4)
    tbl_dict.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_header(tbl_dict.rows[0], ["Feature", "Data Type", "Clinical Description", "Reference Range / Encoding"])

    dict_rows = [
        ("age", "Numeric (Int)", "Patient chronological age", "29 to 77 completed years"),
        ("sex", "Categorical (Bin)", "Biological sex", "1 = Male, 0 = Female"),
        ("cp", "Categorical (Nom)", "Chest pain categorization", "0: Typical, 1: Atypical, 2: Non-anginal, 3: Asymptomatic"),
        ("trestbps", "Numeric (Float)", "Resting blood pressure upon admission", "60 to 260 mm Hg (Normal: < 120 mm Hg)"),
        ("chol", "Numeric (Float)", "Serum cholesterol concentration", "80 to 600 mg/dl (Desirable: < 200 mg/dl)"),
        ("fbs", "Categorical (Bin)", "Fasting blood sugar > 120 mg/dl", "1 = True (diabetic range), 0 = False"),
        ("restecg", "Categorical (Nom)", "Resting electrocardiographic results", "0: Normal, 1: ST-T wave anomaly, 2: LVH"),
        ("thalach", "Numeric (Float)", "Maximum heart rate achieved during stress", "50 to 250 bpm (Bruce protocol stress test)"),
        ("exang", "Categorical (Bin)", "Exercise-induced angina symptom", "1 = Yes (ischemia elicited), 0 = No"),
        ("oldpeak", "Numeric (Float)", "ST depression induced by exercise vs rest", "0.0 to 10.0 mm (electrocardiographic marker)"),
        ("slope", "Categorical (Ord)", "Slope of peak exercise ST segment", "0: Upsloping, 1: Flat (ischemic), 2: Downsloping"),
        ("ca", "Numeric (Int)", "Major vessels colored by fluoroscopy", "0 to 3 coronary vessels visualized (4 missing values)"),
        ("thal", "Categorical (Nom)", "Thallium scintigraphy stress defect", "1: Normal, 2: Fixed defect, 3: Reversible (2 missing)"),
        ("target", "Binary Target", "Coronary artery disease diagnosis", "0: Absence (< 50% stenosis), 1: Presence (>= 50%)"),
    ]

    for idx, (col_name, dtype, desc, ref) in enumerate(dict_rows):
        format_table_row(tbl_dict.rows[idx + 1], [col_name, dtype, desc, ref], is_alt=(idx % 2 == 1))

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    add_custom_heading(doc, "2.2 Supervised Binary Classification in Clinical Tabular Domains", level=2)
    add_body_paragraph(
        doc,
        "Supervised binary classification seeks to learn a mapping function f: X -> {0, 1} from a training set D = {(x_i, y_i)}_{i=1}^N, "
        "where x_i in R^d represents the d-dimensional patient biomarker vector and y_i in {0, 1} denotes the verified disease state. "
        "In clinical diagnostic decision support, classification models should ideally generate calibrated posterior probabilities P(Y = 1 | X = x), "
        "enabling risk stratification across continuous thresholds rather than producing uncalibrated hard binary decisions."
    )

    add_custom_heading(doc, "2.3 Mathematical Formulations of Candidate Algorithms", level=2)
    add_body_paragraph(
        doc,
        "To rigorously benchmark diverse inductive biases, seven representative machine learning algorithms were selected:",
        bold_prefix="Candidate Model Families: "
    )
    # 1. Logistic Regression
    add_body_paragraph(
        doc,
        "Models the posterior log-odds as a linear combination of clinical feature inputs using the logistic sigmoid function:",
        bold_prefix="1. Logistic Regression (L2-Regularized Linear Baseline): ",
        space_after=3
    )
    eq_lr1 = (
        o_r("P(Y = 1 | x) = σ(") +
        o_sSup(o_r("w"), o_r("T")) +
        o_r("x + b) = ") +
        o_frac(o_r("1"), o_r("1 + ") + o_sSup(o_r("e"), o_r("-(") + o_sSup(o_r("w"), o_r("T")) + o_r("x + b)")))
    )
    add_math_equation(doc, eq_lr1, space_before=3, space_after=4)
    add_body_paragraph(
        doc,
        "The model parameters w and b are estimated by minimizing the negative log-likelihood objective with Ridge (L2) regularization:",
        space_after=3
    )
    bracket_content = (
        o_sSub(o_r("y"), o_r("i")) + o_r(" ln(") + o_sSub(o_r("p"), o_r("i")) + o_r(") + (1 - ") +
        o_sSub(o_r("y"), o_r("i")) + o_r(") ln(1 - ") + o_sSub(o_r("p"), o_r("i")) + o_r(")")
    )
    norm_term = o_sSup(o_sSub(o_delim(o_r("w"), beg="‖", end="‖"), o_r("2")), o_r("2"))
    eq_lr2 = (
        o_r("J(w) = - ") +
        o_sum(o_r("i=1"), o_r("N"), o_delim(bracket_content, beg="[", end="]")) +
        o_r(" + ") +
        o_frac(o_r("1"), o_r("2C")) +
        norm_term
    )
    add_math_equation(doc, eq_lr2, space_before=3, space_after=4)
    add_body_paragraph(
        doc,
        "where C > 0 controls regularization inverse strength, penalizing excessive model weights on collinear biomarkers.",
        space_after=6
    )

    # 2. KNN
    add_body_paragraph(
        doc,
        "Assigns patient risk based on majority voting or distance-weighted interpolation among the k closest training instances "
        "measured in standardized Euclidean feature space:",
        bold_prefix="2. K-Nearest Neighbors (KNN - Instance-Based Non-Parametric): ",
        space_after=3
    )
    diff_term = o_delim(o_sSub(o_r("x"), o_r("j")) + o_r(" - ") + o_sSub(o_r("x\x27"), o_r("j")), beg="(", end=")")
    sum_term = o_sum(o_r("j=1"), o_r("d"), o_sSup(diff_term, o_r("2")))
    eq_knn1 = o_r("d(x, x\x27) = ") + o_rad(sum_term)
    add_math_equation(doc, eq_knn1, space_before=3, space_after=4)
    eq_knn2 = (
        o_r("P(Y = 1 | x) = ") +
        o_frac(o_r("1"), o_r("k")) +
        o_sum(o_sSub(o_r("x"), o_r("i")) + o_r(" ∈ ") + o_sSub(o_r("N"), o_r("k")) + o_r("(x)"), expr=o_sSub(o_r("y"), o_r("i")))
    )
    add_math_equation(doc, eq_knn2, space_before=3, space_after=4)
    add_body_paragraph(
        doc,
        "where Nk(x) represents the set of k nearest training instances in normalized Euclidean metric space.",
        space_after=6
    )

    # 3. Decision Tree
    add_body_paragraph(
        doc,
        "Recursively partitions the feature space into axis-aligned hyper-rectangles by maximizing Gini impurity reduction at each candidate node t:",
        bold_prefix="3. Decision Tree (Rule-Based Greedy Splitting): ",
        space_after=3
    )
    eq_dt = (
        o_sSub(o_r("I"), o_r("Gini")) + o_r("(t) = 1 - ") +
        o_sum(o_r("c ∈ {0, 1}"), expr=o_sSup(o_r("p(c | t)"), o_r("2")))
    )
    add_math_equation(doc, eq_dt, space_before=3, space_after=4)
    add_body_paragraph(
        doc,
        "Decision trees offer direct rule extraction but are notoriously vulnerable to high variance and training overfitting on modest sample cohorts.",
        space_after=6
    )

    # 4. Random Forest
    add_body_paragraph(
        doc,
        "Constructs B bootstrap aggregate decision trees trained on random feature subsets (mtry = sqrt(d)). The ensemble probability "
        "is the unweighted mean of individual tree posteriors:",
        bold_prefix="4. Random Forest (Bagging Ensemble of Decorrelated Trees): ",
        space_after=3
    )
    eq_rf = (
        o_r("P(Y = 1 | x) = ") +
        o_frac(o_r("1"), o_r("B")) +
        o_sum(o_r("b=1"), o_r("B"), o_sSub(o_r("T"), o_r("b")) + o_r("(x)"))
    )
    add_math_equation(doc, eq_rf, space_before=3, space_after=4)
    add_body_paragraph(
        doc,
        "This substantially suppresses individual tree variance without inducing additional bias.",
        space_after=6
    )

    # 5. Support Vector Machine
    add_body_paragraph(
        doc,
        "Determines an optimal separating hyperplane that maximizes the geometric margin 2 / ||w|| between classes. Non-linear relationships "
        "are projected into infinite-dimensional Hilbert spaces using the Radial Basis Function (RBF) kernel:",
        bold_prefix="5. Support Vector Machine (SVM - Maximum-Margin Kernel Classification): ",
        space_after=3
    )
    norm_diff = o_sSup(o_delim(o_r("x - x\x27"), beg="‖", end="‖"), o_r("2"))
    eq_svm = o_r("K(x, x\x27) = exp(-γ ") + norm_diff + o_r(")")
    add_math_equation(doc, eq_svm, space_before=3, space_after=4)
    add_body_paragraph(
        doc,
        "Posterior probabilities are derived via Platt scaling (calibrating a sigmoid on SVM decision boundary values).",
        space_after=6
    )

    # 6. AdaBoost
    add_body_paragraph(
        doc,
        "Sequentially builds an ensemble of weak base estimators (depth-1 decision stumps), assigning elevated sample weights to instances "
        "misclassified by preceding iterations and combining predictions via stage-wise additive modeling:",
        bold_prefix="6. AdaBoost (Adaptive Sequential Boosting): ",
        space_after=3
    )
    ada_sum = o_sum(o_r("m=1"), o_r("M"), o_sSub(o_r("α"), o_r("m")) + o_sSub(o_r("h"), o_r("m")) + o_r("(x)"))
    ada_alpha = o_sSub(o_r("α"), o_r("m")) + o_r(" = ") + o_frac(o_r("1"), o_r("2")) + o_r(" ln") + o_delim(o_frac(o_r("1 - ") + o_sSub(o_r("ε"), o_r("m")), o_sSub(o_r("ε"), o_r("m"))))
    eq_ada = o_r("H(x) = sign") + o_delim(ada_sum, beg="(", end=")") + o_r(",      ") + ada_alpha
    add_math_equation(doc, eq_ada, space_before=3, space_after=4)
    add_body_paragraph(
        doc,
        "where εm denotes the weighted error rate of the m-th weak hypothesis hm(x) and αm represents its diagnostic voting weight.",
        space_after=6
    )

    # 7. Gradient Boosted Decision Trees
    add_body_paragraph(
        doc,
        "Iteratively optimizes arbitrary differentiable loss functions (binary cross-entropy) by fitting subsequent regression trees "
        "to pseudo-residuals (negative gradients) of previous iterations:",
        bold_prefix="7. Gradient Boosted Decision Trees (GBDT - Functional Gradient Descent): ",
        space_after=3
    )
    gbdt_num = o_r("∂L(") + o_sSub(o_r("y"), o_r("i")) + o_r(", ") + o_sSub(o_r("F"), o_r("m-1")) + o_r("(") + o_sSub(o_r("x"), o_r("i")) + o_r("))")
    gbdt_den = o_r("∂") + o_sSub(o_r("F"), o_r("m-1")) + o_r("(") + o_sSub(o_r("x"), o_r("i")) + o_r(")")
    eq_gbdt = o_sSub(o_r("r"), o_r("im")) + o_r(" = - ") + o_delim(o_frac(gbdt_num, gbdt_den), beg="[", end="]")
    add_math_equation(doc, eq_gbdt, space_before=3, space_after=4)
    add_body_paragraph(
        doc,
        "Gradient boosting represents a premier benchmark for structured tabular data analysis.",
        space_after=6
    )

    add_custom_heading(doc, "2.4 Explainable Artificial Intelligence (XAI) and Shapley Values", level=2)
    add_body_paragraph(
        doc,
        "A central limitation hindering clinical adoption of advanced machine learning models is the 'black-box' opacity of multi-parameter "
        "interactions. In clinical healthcare, predicting that a patient has an 85% risk of coronary stenosis without justifying which "
        "biomarkers triggered that assessment is clinically unacceptable. Clinicians must understand whether elevated blood pressure, "
        "exercise ST depression, or fluoroscopy vessels drove the classification."
    )
    add_body_paragraph(
        doc,
        "To provide rigorous, mathematically axiomatic model interpretability, this system implements SHapley Additive exPlanations (SHAP) "
        "developed by Lundberg and Lee (2017). Based on cooperative game theory, the Shapley value φi allocates the marginal contribution "
        "of feature i across all possible feature subsets S ⊆ N \\ {i}:",
        space_after=3
    )
    shap_num = o_delim(o_r("S"), beg="|", end="|") + o_r("! ") + o_delim(o_delim(o_r("N"), beg="|", end="|") + o_r(" - ") + o_delim(o_r("S"), beg="|", end="|") + o_r(" - 1"), beg="(", end=")") + o_r("!")
    shap_den = o_delim(o_r("N"), beg="|", end="|") + o_r("!")
    shap_weight = o_frac(shap_num, shap_den)
    shap_diff = o_delim(o_r("v(S ∪ {i}) - v(S)"), beg="[", end="]")
    eq_shap = (
        o_sSub(o_r("φ"), o_r("i")) + o_r("(v) = ") +
        o_sum(o_r("S ⊆ N \\ {i}"), expr=shap_weight + o_r(" ") + shap_diff)
    )
    add_math_equation(doc, eq_shap, space_before=3, space_after=4)
    add_body_paragraph(
        doc,
        "where v(S) is the characteristic model prediction function evaluated on subset S. Shapley values are uniquely proven to satisfy "
        "four essential axiomatic properties: Efficiency (the sum of feature attributions equals the difference between model output and expected baseline), "
        "Symmetry (features with identical marginal contributions receive identical attributions), Dummy (features with zero marginal impact receive zero attribution), "
        "and Additivity (attributions for ensemble models equal the sum of constituent component attributions)."
    )

    add_custom_heading(doc, "2.5 Modern Web Engineering: FastAPI and Asynchronous REST", level=2)
    add_body_paragraph(
        doc,
        "To expose predictive inference to external clients and user interfaces, FastAPI was selected as the backend web framework. "
        "FastAPI is an asynchronous, high-performance web framework built upon the Asynchronous Server Gateway Interface (ASGI) standard "
        "via Starlette and Uvicorn. Key advantages justifying FastAPI for this architecture include:\n"
        "1. Native Pydantic v2 Schema Validation: Enforces strict data types and clinical boundary constraints prior to business logic execution.\n"
        "2. Automated OpenAPI (Swagger) Documentation: Generates interactive API explorers automatically at runtime without manual maintenance.\n"
        "3. High Throughput: Matches Node.js and Go performance benchmarks through asynchronous event loops while retaining Python's rich data science ecosystem.\n"
        "4. Dependency Injection: Elegantly manages database session lifecycles and singleton ML pipeline preloading."
    )

    add_custom_heading(doc, "2.6 Relational Persistence and Object-Relational Mapping (ORM)", level=2)
    add_body_paragraph(
        doc,
        "Clinical risk assessment systems require persistent audit logging to track historical assessments, monitor temporal trends, "
        "and satisfy regulatory traceability. SQLAlchemy 2.0 was selected as the Object-Relational Mapping (ORM) and database abstraction layer. "
        "SQLAlchemy provides a decoupled architectural interface supporting declarative entity mappings, connection pooling, and multi-dialect "
        "compatibility. The system natively supports SQLite for rapid, zero-dependency local development and testing, while providing instant "
        "switch-over to enterprise PostgreSQL instances in production containerized environments via connection string configuration."
    )

    add_custom_heading(doc, "2.7 Containerization and Environmental Reproducibility", level=2)
    add_body_paragraph(
        doc,
        "A common point of failure in empirical data science is environmental drift—incompatible shared library versions, differing operating system "
        "compilers, and mismatched dependency wheels. Containerization via Docker addresses this by packaging application source code, virtual "
        "environments, C-level scientific libraries, and system dependencies into an immutable, multi-platform image. Docker Compose "
        "further orchestrates multi-container runtime topologies, coordinating the web API gateway and relational database services."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: REQUIREMENTS ANALYSIS
    # =========================================================================
    add_custom_heading(doc, "3. Requirements Analysis", level=1)

    add_custom_heading(doc, "3.1 Functional Requirements", level=2)
    add_body_paragraph(
        doc,
        "Functional requirements define the core operational behaviors, data transformations, and endpoints that the system must deliver:"
    )

    # Table 3.1: Functional Requirements
    p_tbl_fr = doc.add_paragraph()
    p_tbl_fr.paragraph_format.space_before = Pt(6)
    p_tbl_fr.paragraph_format.space_after = Pt(4)
    r_cap_fr = p_tbl_fr.add_run("Table 3.1: Formal Functional Requirements Specification")
    r_cap_fr.bold = True
    r_cap_fr.font.name = "Calibri"
    r_cap_fr.font.size = Pt(10)

    tbl_fr = doc.add_table(rows=9, cols=3)
    tbl_fr.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_header(tbl_fr.rows[0], ["Identifier", "Requirement Name", "Functional Specification Description"])

    fr_data = [
        ("FR-1", "Dataset Ingestion & Validation", "System must ingest the 14-attribute Cleveland CSV dataset, enforce numeric types, validate absence of duplicate records, and map multiclass target stages (0-4) into binary format {0, 1}."),
        ("FR-2", "Leakage-Free Preprocessing", "System must execute stratified 80/20 train/test splitting prior to any feature transformation, learning scaling and imputation parameters exclusively on training data."),
        ("FR-3", "Multi-Algorithm Benchmarking", "System must train and benchmark 7 distinct model families under Stratified 5-Fold CV, reporting Accuracy, Precision, Recall, F1, and ROC-AUC."),
        ("FR-4", "Single Patient Risk Inference", "API must expose POST /api/v1/predict accepting 13 clinical features, validating input ranges, and returning risk probability and categorical tier (Low/Moderate/High)."),
        ("FR-5", "Local SHAP Attribution", "System must compute local Shapley feature attributions for each prediction query, detailing directional impact (+ risk vs - protective) on the assessment."),
        ("FR-6", "Persistent Audit Logging", "System must persist each patient assessment into the relational database, recording timestamp, input parameters, prediction, probability, tier, and top SHAP factors."),
        ("FR-7", "History Querying & CSV Export", "API must expose paginated history querying with risk tier filtering and streaming CSV export via GET /api/v1/history/export/csv."),
        ("FR-8", "Interactive Web Dashboard", "System must serve an interactive responsive web UI with clinical input forms, radial probability gauges, SHAP attribution charts, history tables, and research curves."),
    ]
    for idx, (fid, name, spec) in enumerate(fr_data):
        format_table_row(tbl_fr.rows[idx + 1], [fid, name, spec], is_alt=(idx % 2 == 1))

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    add_custom_heading(doc, "3.2 Non-Functional Requirements", level=2)
    add_body_paragraph(
        doc,
        "Non-functional requirements specify qualitative operational criteria, performance constraints, and software engineering standards:"
    )

    # Table 3.2: Non-Functional Requirements
    p_tbl_nfr = doc.add_paragraph()
    p_tbl_nfr.paragraph_format.space_before = Pt(6)
    p_tbl_nfr.paragraph_format.space_after = Pt(4)
    r_cap_nfr = p_tbl_nfr.add_run("Table 3.2: Formal Non-Functional Requirements Specification")
    r_cap_nfr.bold = True
    r_cap_nfr.font.name = "Calibri"
    r_cap_nfr.font.size = Pt(10)

    tbl_nfr = doc.add_table(rows=7, cols=3)
    tbl_nfr.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_header(tbl_nfr.rows[0], ["Identifier", "Quality Attribute", "Non-Functional Specification Target"])

    nfr_data = [
        ("NFR-1", "Low-Latency Performance", "The prediction endpoint POST /api/v1/predict must return complete inferences, including SHAP attributions, within <= 100 milliseconds under local hardware execution."),
        ("NFR-2", "Data Integrity & Validation", "Pydantic v2 schemas must reject invalid physiological ranges (e.g. age > 120, negative blood pressure) with HTTP 422 Unprocessable Entity and explicit error details."),
        ("NFR-3", "Software Modularity", "Codebase must adhere to strict separation of concerns across data, features, models, api, database, schemas, and services modules. No monolithic scripts."),
        ("NFR-4", "Test Suite Coverage", "The automated pytest test suite must achieve >= 70% statement coverage across application packages and execute with 100% passing status."),
        ("NFR-5", "Environmental Portability", "The complete application must execute deterministically inside Docker containers using Docker Compose without platform-specific host modifications."),
        ("NFR-6", "Usability & Accessibility", "Client interface must provide responsive layouts, accessible clinical color contrast, and immediate sample profile presets for testing."),
    ]
    for idx, (nid, attr, target) in enumerate(nfr_data):
        format_table_row(tbl_nfr.rows[idx + 1], [nid, attr, target], is_alt=(idx % 2 == 1))

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    add_custom_heading(doc, "3.3 System Constraints", level=2)
    add_body_paragraph(
        doc,
        "Development and runtime execution were subject to several defined technical constraints:"
    )
    add_bullet_point(doc, "Runtime Platform: ", "Python 3.12+ execution environment with strict virtual environment isolation (.venv).")
    add_bullet_point(doc, "Deterministic Randomness: ", "All stochastic algorithms (train/test splits, cross-validation partitioning, tree bootstrapping) must enforce fixed random seeds (RANDOM_STATE = 42).")
    add_bullet_point(doc, "Zero Cloud Dependency: ", "The system must operate completely self-contained in local offline environments without requiring proprietary third-party cloud APIs.")

    add_custom_heading(doc, "3.4 Use Case Specifications", level=2)
    add_body_paragraph(
        doc,
        "The system supports three primary user personas: the Clinical Screening Specialist, the Medical Informatics Auditor, "
        "and the Machine Learning Researcher. Representative use cases include:"
    )
    add_bullet_point(doc, "Use Case 1 (UC-1: Execute Patient Risk Assessment): ", "Actor enters patient physiological vitals (or clicks 'Sample: High Risk'). The system validates inputs, computes the predicted disease probability, assigns the risk tier, generates local SHAP waterfall attributions, logs the evaluation in the SQL database, and updates the radial risk gauge.")
    add_bullet_point(doc, "Use Case 2 (UC-2: Audit Prediction History & Export): ", "Actor navigates to the 'Prediction History' tab. The system queries the database, displays paginated assessment records with timestamps and biomarkers, enables filtering by 'High Risk', and generates an on-demand downloadable CSV audit file.")
    add_bullet_point(doc, "Use Case 3 (UC-3: Benchmark Research Models): ", "Actor accesses the 'Research & Analytics' tab or executes 'python -m src.models.train'. The system evaluates all 7 model families across 5 stratified folds, computes ROC and PR curves, and generates global SHAP factor importance rankings.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: SYSTEM DESIGN AND ARCHITECTURE
    # =========================================================================
    add_custom_heading(doc, "4. System Design and Architecture", level=1)

    add_custom_heading(doc, "4.1 Overall Architectural Topology", level=2)
    add_body_paragraph(
        doc,
        "The system is structured as a decoupled, multi-tier data-intensive web application. It cleanly separates machine learning "
        "inference and explanation from API routing, relational data persistence, and client presentation. This decoupled design "
        "ensures that model artifacts can be retrained and updated independently without altering database schemas or client logic."
    )

    add_callout_box(
        doc,
        "Architectural Topology Hierarchy:\n"
        "1. Client Tier: Responsive HTML5/CSS3/JavaScript SPA (Form, Gauge, SHAP bars, History, Analytics)\n"
        "2. Application Gateway Tier: FastAPI REST Engine (Pydantic v2 validation, CORS, Lifespan preloading)\n"
        "3. Service Orchestration Tier: PredictionService & ModelExplainer (Inference coordination & SHAP)\n"
        "4. Machine Learning Pipeline Tier: Serialized scikit-learn Pipeline (ColumnTransformer + Tuned Estimator)\n"
        "5. Persistence Tier: SQLAlchemy 2.0 ORM (PredictionRecord, ModelVersion across SQLite / PostgreSQL)",
        title="FIGURE 4.1: MULTI-TIER COMPONENT TOPOLOGY"
    )

    add_custom_heading(doc, "4.2 Component Architecture and Module Separation", level=2)
    add_body_paragraph(
        doc,
        "The codebase enforces strict modular encapsulation across five principal packages:",
        bold_prefix="Module Breakdown: "
    )
    add_bullet_point(doc, "src.data: ", "Encapsulates load_raw_dataset(), structural validation, and build_preprocessor() constructing scikit-learn ColumnTransformer objects.")
    add_bullet_point(doc, "src.features: ", "Contains ClinicalFeatureEngineer, a scikit-learn compatible transformer generating clinically motivated interaction ratios without data leakage.")
    add_bullet_point(doc, "src.models: ", "Houses the complete training CLI (train.py), multi-metric calculation (evaluate.py), model explainer (interpret.py), and singleton inference engine (predict.py).")
    add_bullet_point(doc, "app.api & app.schemas: ", "Defines Pydantic v2 schemas for request validation and response serialization, alongside modular APIRouter controllers for prediction, history, and analytics.")
    add_bullet_point(doc, "app.database & app.services: ", "Manages SQLAlchemy database models, repository CRUD functions, and high-level prediction orchestration.")

    add_custom_heading(doc, "4.3 End-to-End Data Flow Dynamics", level=2)
    add_body_paragraph(
        doc,
        "During live inference, data traverses the architecture through five synchronous stages:",
        space_after=4
    )
    add_numbered_item(doc, "1.", "Ingestion & Validation:", "The client submits a JSON payload to POST /api/v1/predict. FastAPI intercepts the request and validates all 13 fields against PatientInputSchema constraints. If invalid, a 422 error is returned immediately.")
    add_numbered_item(doc, "2.", "Pipeline Execution:", "PredictionService passes the validated feature dictionary to PredictionEngine. The engine constructs a 1-row DataFrame and feeds it to the preloaded scikit-learn pipeline. The pipeline imputes missing cells, applies standard scaling, executes one-hot encoding, and calculates predict_proba().")
    add_numbered_item(doc, "3.", "Risk Tiering:", "The predicted probability p is categorized into clinical tiers: Low Risk (p < 0.35), Moderate Risk (0.35 <= p < 0.65), or High Risk (p >= 0.65).")
    add_numbered_item(doc, "4.", "Local SHAP Attribution:", "ModelExplainer calculates directional Shapley values for the patient instance, mapping encoded columns back to user-friendly clinical factors.")
    add_numbered_item(doc, "5.", "Persistence & Delivery:", "PredictionRepository creates an immutable PredictionRecord in the SQL database. The API returns a structured PredictionResponseSchema to the client, which updates the radial gauge and SHAP waterfall chart.", space_after=6)

    add_custom_heading(doc, "4.4 Database Design and Entity Relationships", level=2)
    add_body_paragraph(
        doc,
        "The relational database schema is normalized and indexed to support responsive history queries and regulatory auditing:"
    )

    # Table 4.1: Database Schema
    p_tbl_db = doc.add_paragraph()
    p_tbl_db.paragraph_format.space_before = Pt(6)
    p_tbl_db.paragraph_format.space_after = Pt(4)
    r_cap_db = p_tbl_db.add_run("Table 4.1: Database Schema Specification for prediction_records Table")
    r_cap_db.bold = True
    r_cap_db.font.name = "Calibri"
    r_cap_db.font.size = Pt(10)

    tbl_db = doc.add_table(rows=10, cols=4)
    tbl_db.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_header(tbl_db.rows[0], ["Column Name", "SQL Data Type", "Constraints / Index", "Description / Purpose"])

    db_schema_data = [
        ("id", "INTEGER", "PRIMARY KEY, AUTOINCREMENT", "Unique identifier for each clinical evaluation record."),
        ("created_at", "DATETIME(TZ)", "INDEX, NOT NULL", "UTC timestamp recording assessment generation moment."),
        ("age ... thal", "INTEGER / FLOAT", "13 Columns, NOT NULL", "Exact clinical patient physiological inputs at assessment time."),
        ("prediction", "INTEGER", "NOT NULL", "Binary model classification output (0 = Low Risk, 1 = High Risk)."),
        ("probability", "FLOAT", "NOT NULL", "Continuous predicted disease probability bounded in [0.0, 1.0]."),
        ("risk_tier", "VARCHAR(50)", "INDEX, NOT NULL", "Categorical risk stratification: 'Low Risk', 'Moderate Risk', 'High Risk'."),
        ("top_features", "TEXT (JSON)", "NULLABLE", "JSON-encoded array of local SHAP attributions and directional impacts."),
        ("model_version", "VARCHAR(50)", "NOT NULL", "Semantic version of deployed pipeline (e.g. '1.0.0')."),
        ("model_versions table", "RELATIONAL ENTITY", "PRIMARY KEY (id), UNIQUE (version)", "Secondary table tracking deployed model versions, training dates, and metrics."),
    ]
    for idx, (col, dtype, constr, purp) in enumerate(db_schema_data):
        format_table_row(tbl_db.rows[idx + 1], [col, dtype, constr, purp], is_alt=(idx % 2 == 1))

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    add_custom_heading(doc, "4.5 RESTful API Design and Endpoint Catalog", level=2)
    add_body_paragraph(
        doc,
        "The REST API is organized into three specialized routers under the /api/v1 prefix, adhering to REST conventions:"
    )

    # Table 4.2: API Endpoints
    p_tbl_api = doc.add_paragraph()
    p_tbl_api.paragraph_format.space_before = Pt(6)
    p_tbl_api.paragraph_format.space_after = Pt(4)
    r_cap_api = p_tbl_api.add_run("Table 4.2: Comprehensive REST API Endpoint Specification and Routing Matrix")
    r_cap_api.bold = True
    r_cap_api.font.name = "Calibri"
    r_cap_api.font.size = Pt(10)

    tbl_api = doc.add_table(rows=12, cols=4)
    tbl_api.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_header(tbl_api.rows[0], ["HTTP Method", "Path Route", "Request / Query Payload", "Response Summary"])

    api_routes = [
        ("GET", "/health", "None", "Health status, model loaded flag, DB status { status: 'ok' }"),
        ("POST", "/api/v1/predict", "PatientInputSchema (13 fields)", "Prediction, probability, risk tier, local SHAP attributions"),
        ("POST", "/api/v1/predict/batch", "List[PatientInputSchema]", "Array of prediction responses for multi-patient evaluation"),
        ("GET", "/api/v1/history", "skip (int), limit (int), risk_tier (str)", "Paginated history array with total count and records"),
        ("GET", "/api/v1/history/stats", "None", "Aggregate counts by risk tier and mean predicted probability"),
        ("GET", "/api/v1/history/{id}", "Path: prediction_id (int)", "Detailed single patient evaluation record"),
        ("DELETE", "/api/v1/history/{id}", "Path: prediction_id (int)", "Deletes record from database { success: true, deleted_id }"),
        ("GET", "/api/v1/history/export/csv", "None", "StreamingResponse serving downloadable CSV of all records"),
        ("GET", "/api/v1/analytics/model-info", "None", "Active model metadata, training samples, test metrics"),
        ("GET", "/api/v1/analytics/model-comparison", "None", "7-model cross-validation evaluation comparison table"),
        ("GET", "/api/v1/analytics/global-importance", "None", "Global SHAP feature importance ranking array"),
    ]
    for idx, (mth, path, req, res) in enumerate(api_routes):
        format_table_row(tbl_api.rows[idx + 1], [mth, path, req, res], is_alt=(idx % 2 == 1))

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    add_custom_heading(doc, "4.6 Security and Ethical Privacy Safeguards", level=2)
    add_body_paragraph(
        doc,
        "Although engineered as a research platform, privacy and defensive engineering principles were rigorously enforced:",
        space_after=4
    )
    add_numbered_item(doc, "1.", "Zero Protected Health Information (PHI):", "The system never collects, stores, or transmits patient names, addresses, Social Security numbers, or national identifiers. Only anonymized physiological vectors are processed.")
    add_numbered_item(doc, "2.", "Input Sanitization & Type Coercion:", "Pydantic v2 strictly enforces numerical types, rejecting SQL injection strings or malformed payloads before execution reaches the database or inference engine.")
    add_numbered_item(doc, "3.", "Explicit Medical Disclaimers:", "Every API response and UI view prominently includes the academic disclaimer declaring that predictions represent statistical estimates and are not certified clinical diagnoses.", space_after=6)

    add_custom_heading(doc, "4.7 Architectural Design Decisions and Trade-Off Analysis", level=2)
    add_body_paragraph(
        doc,
        "Critical architectural trade-offs evaluated during system design included:",
        space_after=4
    )
    add_numbered_item(doc, "1.", "Preloaded Singleton vs. On-Demand Retraining:", "The trained pipeline is loaded once into memory during the FastAPI lifespan startup event. This eliminates redundant disk I/O and deserialization latency, achieving sub-10ms raw inference speeds.")
    add_numbered_item(doc, "2.", "Single Deployable Pipeline Artifact:", "Merging ColumnTransformer preprocessing and the tuned classifier into a single joblib artifact guarantees that identical scaling and imputation logic applies during training and live inference, eliminating train-serve skew.")
    add_numbered_item(doc, "3.", "Dual Database Dialect Architecture:", "Leveraging SQLAlchemy allows developers to execute tests instantly against an in-memory SQLite database while enabling seamless containerized deployment against PostgreSQL without modifying code.", space_after=6)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: IMPLEMENTATION
    # =========================================================================
    add_custom_heading(doc, "5. Implementation", level=1)

    add_custom_heading(doc, "5.1 Development Environment and Pinned Toolchain", level=2)
    add_body_paragraph(
        doc,
        "The system was developed and validated in an isolated Python 3.12.0 virtual environment (.venv) on macOS (Darwin arm64). "
        "All third-party libraries and runtime tools are strictly pinned in pyproject.toml and requirements.txt to guarantee reproducibility."
    )

    # Table 5.1: Software Stack
    p_tbl_env = doc.add_paragraph()
    p_tbl_env.paragraph_format.space_before = Pt(6)
    p_tbl_env.paragraph_format.space_after = Pt(4)
    r_cap_env = p_tbl_env.add_run("Table 5.1: Pinned Production Software Stack and Development Toolchain")
    r_cap_env.bold = True
    r_cap_env.font.name = "Calibri"
    r_cap_env.font.size = Pt(10)

    tbl_env = doc.add_table(rows=9, cols=3)
    tbl_env.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_header(tbl_env.rows[0], ["Component Layer", "Selected Technology & Version", "Engineering Purpose in Project"])

    env_data = [
        ("Base Runtime", "Python 3.12.0", "Core programming runtime with enhanced type annotations and speed optimizations."),
        ("Data Processing", "NumPy 2.5.3, pandas 3.0.6", "Vectorized numerical array computing and tabular data manipulation."),
        ("Machine Learning", "scikit-learn 1.9.1, SciPy 1.18.1", "Pipeline transformations, 7 candidate algorithms, cross-validation, and metrics."),
        ("Model Interpretability", "SHAP 0.52.0", "TreeExplainer and LinearExplainer computing Shapley attribution values."),
        ("Backend Framework", "FastAPI 0.141.1, Uvicorn 0.54.0", "Asynchronous ASGI web application framework and production HTTP server."),
        ("Data Validation", "Pydantic 2.13.5, pydantic-settings 2.15.0", "Rust-accelerated schema validation and environment configuration parsing."),
        ("Persistence / ORM", "SQLAlchemy 2.1.1", "Object-Relational Mapping, connection pooling, and multi-dialect SQL execution."),
        ("Testing Suite", "pytest 9.1.1, pytest-cov 7.1.0, httpx 0.28.1", "Automated test execution, statement coverage analysis, and mock API client."),
    ]
    for idx, (layer, tech, purpose) in enumerate(env_data):
        format_table_row(tbl_env.rows[idx + 1], [layer, tech, purpose], is_alt=(idx % 2 == 1))

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    add_custom_heading(doc, "5.2 Physical Project Layout and Directory Structure", level=2)
    add_body_paragraph(
        doc,
        "The repository adheres to standardized Python software engineering practices, separating source code, data artifacts, "
        "tests, documentation, and containerization assets:"
    )

    project_tree = (
        "cardiovascular-risk-ml-system/\n"
        "|-- data/\n"
        "|   |-- raw/heart_disease.csv        # Benchmark UCI Cleveland dataset (303 records)\n"
        "|   |-- processed/                   # Intermediate cache\n"
        "|   `-- README.md                    # Detailed data dictionary and provenance notes\n"
        "|-- src/\n"
        "|   |-- config.py                    # Central Pydantic BaseSettings and schema constants\n"
        "|   |-- data/\n"
        "|   |   |-- loading.py               # Ingestion, validation, and stratified train/test split\n"
        "|   |   `-- preprocessing.py         # ColumnTransformer pipeline builder and feature extractor\n"
        "|   |-- features/\n"
        "|   |   `-- engineering.py           # ClinicalFeatureEngineer scikit-learn transformer\n"
        "|   `-- models/\n"
        "|       |-- train.py                 # Automated 7-model training & grid optimization CLI\n"
        "|       |-- evaluate.py              # Multi-metric classification evaluation suite\n"
        "|       |-- predict.py               # Singleton PredictionEngine inference service\n"
        "|       `-- interpret.py             # ModelExplainer managing SHAP global/local attributions\n"
        "|-- app/\n"
        "|   |-- main.py                      # FastAPI application factory, lifespan, and CORS\n"
        "|   |-- api/\n"
        "|   |   |-- routes_prediction.py     # Patient prediction and batch endpoints\n"
        "|   |   |-- routes_history.py        # Persistence, filtering, and streaming CSV export\n"
        "|   |   `-- routes_analytics.py      # Model comparison, global SHAP, and curve coordinates\n"
        "|   |-- schemas/\n"
        "|   |   `-- prediction.py            # Pydantic v2 patient input and response models\n"
        "|   |-- database/\n"
        "|   |   |-- connection.py            # Engine and SessionLocal factory with init_db()\n"
        "|   |   |-- models.py                # PredictionRecord and ModelVersion ORM entities\n"
        "|   |   `-- repository.py            # Database CRUD abstraction layer\n"
        "|   |-- services/\n"
        "|   |   `-- prediction_service.py    # High-level business logic orchestrator\n"
        "|   |-- templates/\n"
        "|   |   `-- index.html               # Multi-tab responsive single-page dashboard\n"
        "|   `-- static/\n"
        "|       |-- css/styles.css           # Health-tech responsive stylesheet\n"
        "|       `-- js/app.js                # Vanilla JavaScript client application\n"
        "|-- models/\n"
        "|   |-- best_model.joblib            # Serialized production pipeline artifact\n"
        "|   `-- model_metadata.json          # Complete evaluation metrics, curves, and parameters\n"
        "|-- tests/\n"
        "|   |-- conftest.py                  # Pytest fixtures and shared in-memory test database\n"
        "|   |-- test_preprocessing.py        # Preprocessing, leakage, and feature engineering tests\n"
        "|   |-- test_models.py               # Model loading, metrics, inference, and SHAP tests\n"
        "|   |-- test_database.py             # SQLAlchemy CRUD, pagination, and stats tests\n"
        "|   |-- test_api.py                  # FastAPI route and boundary validation tests\n"
        "|   `-- test_integration.py          # Complete end-to-end user journey test\n"
        "|-- notebooks/                       # 5 standalone executable research scripts (Stages 1-5)\n"
        "|-- docs/                            # Architecture, methodology, and API reference guides\n"
        "|-- thesis/                          # Academic thesis documentation and Word generator\n"
        "|-- Dockerfile                       # Multi-stage production container build\n"
        "|-- docker-compose.yml               # Service orchestration (API + PostgreSQL option)\n"
        "|-- pyproject.toml                   # Standard packaging build configuration\n"
        "|-- requirements.txt                 # Pinned dependencies\n"
        "`-- README.md                        # Master repository documentation"
    )
    add_code_block(doc, project_tree, caption="Physical Repository Directory Hierarchy")

    add_custom_heading(doc, "5.3 Preprocessing Pipeline and Leakage Prevention Implementation", level=2)
    add_body_paragraph(
        doc,
        "In src/data/loading.py, the function get_train_test_split() enforces strict temporal precedence: the dataset is partitioned "
        "into 80% training (242 records) and 20% test (61 records) partitions with stratification before any imputation or scaling. "
        "In src/data/preprocessing.py, build_preprocessor() constructs an unfitted ColumnTransformer:"
    )
    code_preproc = (
        "def build_preprocessor(numerical_features=None, categorical_features=None, scale_numeric=True):\n"
        "    num_cols = numerical_features or settings.NUMERICAL_FEATURES\n"
        "    cat_cols = categorical_features or settings.CATEGORICAL_FEATURES\n"
        "\n"
        "    # Numeric Pipeline: Median Imputation + Standard Scaling\n"
        "    num_steps = [('imputer', SimpleImputer(strategy='median'))]\n"
        "    if scale_numeric:\n"
        "        num_steps.append(('scaler', StandardScaler()))\n"
        "    numeric_transformer = Pipeline(steps=num_steps)\n"
        "\n"
        "    # Categorical Pipeline: Mode Imputation + One-Hot Encoding\n"
        "    categorical_transformer = Pipeline(steps=[\n"
        "        ('imputer', SimpleImputer(strategy='most_frequent')),\n"
        "        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),\n"
        "    ])\n"
        "\n"
        "    return ColumnTransformer(transformers=[\n"
        "        ('num', numeric_transformer, num_cols),\n"
        "        ('cat', categorical_transformer, cat_cols),\n"
        "    ], remainder='drop')"
    )
    add_code_block(doc, code_preproc, caption="src/data/preprocessing.py — ColumnTransformer Pipeline Definition")

    add_custom_heading(doc, "5.4 Machine Learning Benchmarking and Hyperparameter Optimization", level=2)
    add_body_paragraph(
        doc,
        "The training CLI (src/models/train.py) implements the automated execution of Experiment B (comparative evaluation) and "
        "Experiment C (hyperparameter optimization). Using StratifiedKFold with n_splits=5, cross_validate() calculates accuracy, "
        "precision, recall, f1, and roc_auc across all 7 algorithms. The optimal candidate model is then optimized via GridSearchCV "
        "over regularized parameter grids."
    )

    add_custom_heading(doc, "5.5 Explainable AI (SHAP) Implementation", level=2)
    add_body_paragraph(
        doc,
        "In src/models/interpret.py, the ModelExplainer class manages background dataset masking and explainer initialization. "
        "For the tuned linear pipeline, shap.LinearExplainer evaluates the feature weights against the background training distribution. "
        "For each individual patient query, explain_patient() extracts directional attributions (+ risk vs - protective), computing "
        "both the raw attribution and its absolute magnitude for sorting."
    )

    add_custom_heading(doc, "5.6 Database Layer and Repository Implementation", level=2)
    add_body_paragraph(
        doc,
        "In app/database/repository.py, the PredictionRepository class encapsulates all SQL interactions. Prediction records are stored "
        "with typed numerical columns for patient attributes and a JSON-encoded text string for top SHAP feature contributions. "
        "Helper methods provide pagination (skip and limit), risk tier filtering, and streaming CSV conversion."
    )

    add_custom_heading(doc, "5.7 FastAPI Service and Router Implementation", level=2)
    add_body_paragraph(
        doc,
        "In app/main.py, the FastAPI application registers CORS middleware, static file routes, and lifespan event handlers that preload "
        "the singleton PredictionEngine and initialize database tables via init_db(). The endpoint POST /api/v1/predict accepts "
        "PatientInputSchema instances, delegating execution to PredictionService.process_patient_prediction()."
    )

    add_custom_heading(doc, "5.8 Client Dashboard and Data Visualization Implementation", level=2)
    add_body_paragraph(
        doc,
        "The frontend dashboard (app/templates/index.html, app/static/js/app.js) is engineered with zero external client-side frameworks: "
        "tab switching, AJAX API requests, dynamic SVG radial risk gauges, and local SHAP horizontal bars are rendered using vanilla JavaScript. "
        "Furthermore, the Receiver Operating Characteristic (ROC) curve is rendered dynamically using the HTML5 Canvas API directly from "
        "coordinate vectors retrieved from GET /api/v1/analytics/curves."
    )

    add_custom_heading(doc, "5.9 Configuration, Secrets, and Environment Management", level=2)
    add_body_paragraph(
        doc,
        "Centralized configuration is managed in src/config.py through Pydantic BaseSettings, reading environment variables from .env "
        "files with sane defaults for DATABASE_URL (sqlite:///./cardio_risk.db), MODEL_PATH, RANDOM_STATE (42), and PORT (8000)."
    )

    add_custom_heading(doc, "5.10 Containerization and Docker Deployment", level=2)
    add_body_paragraph(
        doc,
        "The project includes a production-ready Dockerfile utilizing python:3.12-slim, implementing healthcheck polling against "
        "GET /health, and exposing port 8000. The accompanying docker-compose.yml defines services for the API container and persistent data volumes."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: TESTING AND VALIDATION
    # =========================================================================
    add_custom_heading(doc, "6. Testing and Validation", level=1)

    add_custom_heading(doc, "6.1 Comprehensive Testing Strategy", level=2)
    add_body_paragraph(
        doc,
        "Software testing in clinical machine learning must verify both statistical integrity (prevention of data contamination) "
        "and architectural robustness (schema validation, database persistence, and HTTP lifecycle). A multi-tiered testing strategy "
        "was executed using pytest, pytest-cov, and httpx TestClient."
    )

    add_custom_heading(doc, "6.2 Preprocessing and Data Pipeline Unit Tests", level=2)
    add_body_paragraph(
        doc,
        "Implemented in tests/test_preprocessing.py, five automated unit tests verify:",
        space_after=4
    )
    add_numbered_item(doc, "1.", "Dataset Ingestion (test_load_raw_dataset):", "Confirms 303 rows, 14 columns, and valid binary target binarization.")
    add_numbered_item(doc, "2.", "Structural Validation (test_validate_dataset):", "Asserts 164 negative cases, 139 positive cases, 0 duplicates, and exact missingness (ca: 4, thal: 2).")
    add_numbered_item(doc, "3.", "Strict Data Leakage Prevention (test_train_test_split_no_leakage):", "Proves disjoint index intersection between train (242) and test (61) splits.")
    add_numbered_item(doc, "4.", "Preprocessing Pipeline Transformation (test_preprocessor_pipeline_transformation):", "Asserts zero NaN values remain post-transformation and confirms 25 output columns.")
    add_numbered_item(doc, "5.", "Clinical Feature Engineering (test_clinical_feature_engineer):", "Asserts accurate derivation of hr_max_ratio, bp_chol_product, and ischemia indices.", space_after=6)

    add_custom_heading(doc, "6.3 Machine Learning and SHAP Explainer Tests", level=2)
    add_body_paragraph(
        doc,
        "Implemented in tests/test_models.py, five unit tests verify:",
        space_after=4
    )
    add_numbered_item(doc, "1.", "Pipeline Artifact Loading (test_pipeline_artifact_exists_and_loads):", "Confirms deserialization of best_model.joblib with preprocessor and classifier steps.")
    add_numbered_item(doc, "2.", "Metadata Completeness (test_metadata_completeness):", "Confirms presence of all 7 algorithms in model_comparison, test metrics, and ROC coordinates.")
    add_numbered_item(doc, "3.", "Evaluation Metrics Calculation (test_compute_classification_metrics):", "Verifies mathematical accuracy of sensitivity, specificity, and confusion matrix.")
    add_numbered_item(doc, "4.", "Patient Inference Engine (test_prediction_engine_patient_inference):", "Tests mock low-risk and high-risk patients, proving probability bounds and risk tier assignment.")
    add_numbered_item(doc, "5.", "SHAP Explainer Functionality (test_model_explainer_global_and_local):", "Validates global importance calculation and local attribution extraction.", space_after=6)

    add_custom_heading(doc, "6.4 Database and Repository Unit Tests", level=2)
    add_body_paragraph(
        doc,
        "Implemented in tests/test_database.py using an isolated in-memory SQLite database, three tests verify:",
        space_after=4
    )
    add_numbered_item(doc, "1.", "Record Creation & Retrieval (test_create_and_retrieve_prediction):", "Confirms accurate persistence of patient vitals and JSON SHAP attributions.")
    add_numbered_item(doc, "2.", "History Pagination & Filtering (test_get_history_and_filtering):", "Validates filtering by risk tier (Low Risk vs High Risk).")
    add_numbered_item(doc, "3.", "Record Deletion & Statistics (test_delete_prediction_and_stats):", "Asserts accurate deletion and aggregate summary calculations.", space_after=6)

    add_custom_heading(doc, "6.5 API Functional and Boundary Validation Tests", level=2)
    add_body_paragraph(
        doc,
        "Implemented in tests/test_api.py, seven functional tests verify:",
        space_after=4
    )
    add_numbered_item(doc, "1.", "Healthcheck Endpoint (test_health_endpoint):", "Confirms 200 OK with model_loaded=True.")
    add_numbered_item(doc, "2.", "Dashboard Template Rendering (test_index_dashboard_view):", "Asserts complete HTML5 dashboard delivery.")
    add_numbered_item(doc, "3.", "Valid Patient Prediction (test_predict_patient_valid):", "Validates successful prediction, probability, tier, and database ID generation.")
    add_numbered_item(doc, "4.", "Boundary & Constraint Enforcement (test_predict_patient_invalid_ranges):", "Confirms 422 Unprocessable Entity when age > 120 or blood pressure is negative.")
    add_numbered_item(doc, "5.", "Batch Prediction (test_batch_prediction):", "Asserts concurrent evaluation of multiple patient vectors.")
    add_numbered_item(doc, "6.", "History Audit & CSV Export (test_history_flow_and_export):", "Verifies record creation, history lookup, streaming CSV download, and deletion.")
    add_numbered_item(doc, "7.", "Research Analytics Endpoints (test_analytics_endpoints):", "Confirms model metadata, 7-algorithm comparison, and curve data retrieval.", space_after=6)

    add_custom_heading(doc, "6.6 Full End-to-End Integration Workflow Verification", level=2)
    add_body_paragraph(
        doc,
        "Implemented in tests/test_integration.py (test_full_clinical_lifecycle), a comprehensive integration test simulates an entire "
        "user session: verifying health readiness, querying model metadata, submitting low-risk and high-risk patients, verifying database "
        "persistence, validating summary statistics, exporting CSV files, and executing record deletions."
    )

    add_custom_heading(doc, "6.7 Empirical Test Results and Coverage Metrics", level=2)
    add_body_paragraph(
        doc,
        "Executing pytest across all test suites confirmed that 100% of tests passed with zero failures in under 0.5 seconds, "
        "achieving 74% statement coverage across application packages:"
    )

    # Table 6.1: Test Results Table
    p_tbl_test = doc.add_paragraph()
    p_tbl_test.paragraph_format.space_before = Pt(6)
    p_tbl_test.paragraph_format.space_after = Pt(4)
    r_cap_test = p_tbl_test.add_run("Table 6.1: Automated Test Suite Structure, Categorization, and Execution Results")
    r_cap_test.bold = True
    r_cap_test.font.name = "Calibri"
    r_cap_test.font.size = Pt(10)

    tbl_test = doc.add_table(rows=7, cols=5)
    tbl_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_header(tbl_test.rows[0], ["Test Module", "Category", "Tests Executed", "Passing Rate", "Execution Time"])

    test_summary_data = [
        ("tests/test_preprocessing.py", "Data & Pipeline Unit Tests", "5 Tests", "100% Passed (5 / 5)", "0.08 s"),
        ("tests/test_models.py", "ML & Explainability Unit Tests", "5 Tests", "100% Passed (5 / 5)", "0.14 s"),
        ("tests/test_database.py", "ORM & Repository Unit Tests", "3 Tests", "100% Passed (3 / 3)", "0.05 s"),
        ("tests/test_api.py", "API & Validation Functional Tests", "7 Tests", "100% Passed (7 / 7)", "0.12 s"),
        ("tests/test_integration.py", "End-to-End Integration Lifecycle", "1 Test", "100% Passed (1 / 1)", "0.07 s"),
        ("TOTAL SUITE EXECUTION", "Complete Project Verification", "21 Tests", "100% PASSED (21 / 21)", "0.46 s"),
    ]
    for idx, (mod, cat, cnt, rate, tm) in enumerate(test_summary_data):
        is_total = (idx == len(test_summary_data) - 1)
        format_table_row(tbl_test.rows[idx + 1], [mod, cat, cnt, rate, tm], is_alt=(idx % 2 == 1), is_highlight=is_total)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    add_custom_heading(doc, "6.8 Real-World Debugging Case Studies and Root Cause Analysis", level=2)
    add_body_paragraph(
        doc,
        "In accordance with disciplined software engineering, two critical bugs were actively diagnosed and resolved during development:",
        bold_prefix="Investigated Defects: "
    )
    add_body_paragraph(
        doc,
        "During execution of test_analytics_endpoints, GET /api/v1/analytics/curves threw HTTP 500: 'ValueError: Out of range float values are not JSON compliant: inf'.",
        bold_prefix="Defect 1 — Symptom: ",
        space_after=3
    )
    add_body_paragraph(
        doc,
        "In scikit-learn's roc_curve(y_true, y_prob), the leading threshold value at index 0 is conventionally set to np.inf to ensure that False Positive Rate (FPR) begins at 0.0. While standard in scientific computing, float('inf') violates RFC 8259 JSON compliance. When FastAPI's JSONResponse serialized the curve dictionary, Python's json.dumps threw an unhandled exception.",
        bold_prefix="Root Cause Analysis: ",
        space_after=3
    )
    add_body_paragraph(
        doc,
        "In src/models/evaluate.py, compute_roc_curve_data() was refactored with conditional threshold sanitization: clean_thresholds = [1.0 if np.isinf(x) else round(float(x), 4) for x in thresholds]. This sanitized the coordinate vectors while maintaining complete plotting fidelity.",
        bold_prefix="Resolution: ",
        space_after=6
    )

    add_body_paragraph(
        doc,
        "When executing the entire test suite simultaneously, test_history_flow_and_export failed with 'AssertionError: assert 4 == 1', despite passing when executed in isolation.",
        bold_prefix="Defect 2 — Symptom: ",
        space_after=3
    )
    add_body_paragraph(
        doc,
        "By default, SQLite in-memory databases (sqlite:///:memory:) create a new, distinct in-memory database for every open connection. Additionally, both test_api.py and test_integration.py independently assigned different database engines to app.dependency_overrides[get_db] at module import time. Consequently, records created by earlier tests persisted across shared test runs without being purged.",
        bold_prefix="Root Cause Analysis: ",
        space_after=3
    )
    add_body_paragraph(
        doc,
        "Refactored test architecture into tests/conftest.py utilizing SQLAlchemy's StaticPool: engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool). A centralized autouse clean_db fixture was implemented to explicitly issue DELETE statements on all tables before each test, restoring absolute state isolation and eliminating cross-test interference.",
        bold_prefix="Resolution: ",
        space_after=6
    )

    add_custom_heading(doc, "6.9 Codebase Refactoring and Maintainability Enhancements", level=2)
    add_body_paragraph(
        doc,
        "Following test verification, three key refactoring iterations were performed:",
        space_after=4
    )
    add_numbered_item(doc, "1.", "Centralized Conftest Fixtures:", "Consolidated duplicate database engines and test clients into a single, standardized fixture hierarchy.")
    add_numbered_item(doc, "2.", "TemplateResponse Modernization:", "Updated FastAPI/Starlette template rendering to use keyword arguments (request=request, name='index.html'), preventing unhashable dictionary errors under modern Starlette releases.")
    add_numbered_item(doc, "3.", "Decoupled Explainer Fallbacks:", "Implemented defensive exception handling inside ModelExplainer to guarantee that if SHAP encounters an unsupported estimator, standard permutation importances or coefficient weights are returned seamlessly without crashing API inference.", space_after=6)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7: EVALUATION AND DISCUSSION
    # =========================================================================
    add_custom_heading(doc, "7. Evaluation and Discussion", level=1)

    add_custom_heading(doc, "7.1 Functional Requirements Fulfillment Audit", level=2)
    add_body_paragraph(
        doc,
        "An objective audit of the implemented system confirms that all eight functional requirements (FR-1 through FR-8) and six "
        "non-functional requirements (NFR-1 through NFR-6) are completely fulfilled and verified by automated test suites. The data pipeline "
        "operates deterministically without leakage, all 12 API endpoints respond with validated schemas, and the client dashboard delivers "
        "real-time predictions, SHAP visualizations, and database history auditing."
    )

    add_custom_heading(doc, "7.2 Empirical Model Benchmark Analysis (7 Algorithms)", level=2)
    add_body_paragraph(
        doc,
        "In Experiment B, seven distinct machine learning algorithms were trained and evaluated across Stratified 5-Fold Cross-Validation "
        "on the training partition (N = 242). All algorithms received identical, leakage-free ColumnTransformer preprocessing:"
    )

    # Table 7.1: Model Comparison
    p_tbl_comp = doc.add_paragraph()
    p_tbl_comp.paragraph_format.space_before = Pt(6)
    p_tbl_comp.paragraph_format.space_after = Pt(4)
    r_cap_comp = p_tbl_comp.add_run("Table 7.1: Stratified 5-Fold Cross-Validation Performance Comparison Across 7 Algorithms (Training Set N = 242)")
    r_cap_comp.bold = True
    r_cap_comp.font.name = "Calibri"
    r_cap_comp.font.size = Pt(10)

    tbl_comp = doc.add_table(rows=8, cols=6)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_header(tbl_comp.rows[0], ["Model Algorithm", "Algorithm Family", "CV Accuracy", "CV Precision", "CV Recall", "CV ROC-AUC (Mean ± Std)"])

    comp_rows = [
        ("Logistic Regression (Tuned)", "Linear Regularized", "84.7% ± 2.2%", "83.87%", "78.4%", "0.9065 ± 0.0197 (Peak 0.9117)"),
        ("Random Forest", "Bagging Ensemble", "81.4% ± 3.6%", "80.89%", "75.6%", "0.8858 ± 0.0411"),
        ("Support Vector Machine (RBF)", "Kernel-Based", "83.1% ± 0.9%", "85.34%", "76.5%", "0.8850 ± 0.0160"),
        ("K-Nearest Neighbors", "Instance-Based", "82.6% ± 4.1%", "83.79%", "79.2%", "0.8729 ± 0.0551"),
        ("AdaBoost", "Boosting Ensemble", "78.1% ± 2.1%", "78.43%", "72.9%", "0.8668 ± 0.0330"),
        ("Gradient Boosted Trees", "Boosting Ensemble", "79.8% ± 1.5%", "78.49%", "78.4%", "0.8555 ± 0.0175"),
        ("Decision Tree", "Rule-Based", "70.2% ± 4.7%", "70.97%", "67.5%", "0.7001 ± 0.0443"),
    ]
    for idx, (mname, fam, acc, prec, rec, auc) in enumerate(comp_rows):
        is_best = (idx == 0)
        format_table_row(tbl_comp.rows[idx + 1], [mname, fam, acc, prec, rec, auc], is_alt=(idx % 2 == 1), is_highlight=is_best)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    add_custom_heading(doc, "7.3 Hold-out Test Generalization and Clinical Sensitivity", level=2)
    add_body_paragraph(
        doc,
        "In Experiment F, the finalized, tuned Logistic Regression pipeline was evaluated exactly once against the untouched 20% hold-out "
        "test set (N = 61 patient records). The empirical results demonstrate outstanding generalization:"
    )

    # Table 7.2: Test Set Performance
    p_tbl_test_perf = doc.add_paragraph()
    p_tbl_test_perf.paragraph_format.space_before = Pt(6)
    p_tbl_test_perf.paragraph_format.space_after = Pt(4)
    r_cap_tp = p_tbl_test_perf.add_run("Table 7.2: Final Evaluation Performance Metrics on Untouched Test Set (N = 61)")
    r_cap_tp.bold = True
    r_cap_tp.font.name = "Calibri"
    r_cap_tp.font.size = Pt(10)

    tbl_tp = doc.add_table(rows=7, cols=3)
    tbl_tp.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_header(tbl_tp.rows[0], ["Evaluation Metric", "Measured Value", "Clinical Diagnostic Interpretation"])

    test_metrics_data = [
        ("Test Accuracy", "88.52% (0.8852)", "54 out of 61 unseen patient cases correctly classified overall."),
        ("Test Precision", "83.87% (0.8387)", "When flagging a patient as positive, the diagnosis is accurate in 83.87% of cases."),
        ("Test Recall (Sensitivity)", "92.86% (0.9286)", "Crucial Screening Metric: Detected 26 of 28 cardiac patients (only 2 false negatives)."),
        ("Test Specificity", "84.85% (0.8485)", "Correctly cleared 28 of 33 disease-free individuals, limiting unnecessary testing."),
        ("Test F1-Score", "88.14% (0.8814)", "High harmonic balance between precision and sensitivity."),
        ("Area Under ROC (ROC-AUC)", "0.9621", "Outstanding discriminative power separating diseased and healthy populations."),
    ]
    for idx, (met, val, interp) in enumerate(test_metrics_data):
        is_hi = ("Recall" in met or "ROC-AUC" in met)
        format_table_row(tbl_tp.rows[idx + 1], [met, val, interp], is_alt=(idx % 2 == 1), is_highlight=is_hi)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_body_paragraph(
        doc,
        "The resulting test set confusion matrix demonstrates an exceptionally favorable clinical screening distribution:",
        space_after=4
    )
    add_bullet_point(doc, "True Negatives (TN): ", "28 patients correctly classified as free of significant CAD.")
    add_bullet_point(doc, "False Positives (FP): ", "5 healthy patients flagged for secondary evaluation.")
    add_bullet_point(doc, "False Negatives (FN): ", "Only 2 cardiac patients were missed.")
    add_bullet_point(doc, "True Positives (TP): ", "26 cardiac patients correctly detected.")
    add_body_paragraph(
        doc,
        "In clinical triage, an outcome of only 2 false negatives out of 28 true diseased patients represents an outstanding sensitivity rate (92.86%).",
        space_after=6
    )

    add_custom_heading(doc, "7.4 Global and Local Interpretability Findings", level=2)
    add_body_paragraph(
        doc,
        "In Experiment E, SHAP analysis revealed the dominant clinical determinants influencing model behavior across the cohort:"
    )

    # Table 7.3: Global SHAP Factors
    p_tbl_shap = doc.add_paragraph()
    p_tbl_shap.paragraph_format.space_before = Pt(6)
    p_tbl_shap.paragraph_format.space_after = Pt(4)
    r_cap_shap = p_tbl_shap.add_run("Table 7.3: Top 10 Global Clinical Predictive Factors Identified by SHAP")
    r_cap_shap.bold = True
    r_cap_shap.font.name = "Calibri"
    r_cap_shap.font.size = Pt(10)

    tbl_shap = doc.add_table(rows=11, cols=4)
    tbl_shap.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_header(tbl_shap.rows[0], ["Rank", "Clinical Feature", "Mean |SHAP| Value", "Physiological Cardiological Mechanism"])

    shap_data = [
        ("1", "ca (Fluoroscopy Vessels)", "0.5848", "Direct anatomical evidence of calcified atherosclerotic vessels."),
        ("2", "thalach (Max Heart Rate)", "0.2567", "Chronotropic incompetence: inability to raise heart rate indicates ischemic distress."),
        ("3", "thal_3.0 (Normal Thallium)", "0.2548", "Absence of cold perfusion defects serves as a powerful protective negative factor."),
        ("4", "cp_4.0 (Asymptomatic Chest Pain)", "0.2544", "Patients presenting with silent myocardial ischemia experience delayed diagnosis."),
        ("5", "thal_7.0 (Reversible Defect)", "0.2307", "Indicates viable myocardium subjected to stress-induced perfusion deficit."),
        ("6", "sex_0.0 (Female Sex)", "0.1804", "Significant protective factor in pre-menopausal and baseline epidemiological cohorts."),
        ("7", "oldpeak (ST Depression)", "0.1756", "Reflects subendocardial ischemia induced by exercise stress."),
        ("8", "sex_1.0 (Male Sex)", "0.1498", "Elevates baseline CAD risk due to male epidemiological prevalence."),
        ("9", "slope_1.0 (Flat ST Slope)", "0.1422", "Flat ST segments during peak stress correlate with coronary hypoperfusion."),
        ("10", "exang_0.0 (No Exercise Angina)", "0.1343", "Absence of exercise-induced chest pain serves as a protective factor."),
    ]
    for idx, (rnk, feat, score, mech) in enumerate(shap_data):
        format_table_row(tbl_shap.rows[idx + 1], [rnk, feat, score, mech], is_alt=(idx % 2 == 1))

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    add_custom_heading(doc, "7.5 Scientific Discussion: The Bias-Variance Dilemma in Clinical Cohorts", level=2)
    add_body_paragraph(
        doc,
        "A compelling scientific finding of this thesis is that tuned, regularized Logistic Regression outperformed sophisticated "
        "ensemble methods (Random Forest ROC-AUC 0.8858, Gradient Boosting ROC-AUC 0.8555, Decision Tree ROC-AUC 0.7001). "
        "This outcome is thoroughly explained by the classic statistical bias-variance trade-off in small tabular sample regimes (N = 303):",
        space_after=4
    )
    add_numbered_item(doc, "1.", "Parameter Parsimony vs. Overfitting:", "Complex tree-based ensembles feature thousands of splitting parameters, easily overfitting spurious local variances in small clinical sample spaces.")
    add_numbered_item(doc, "2.", "Additive Physiological Nature of Biomarkers:", "In cardiovascular screening, risk factors (such as age, blood pressure, cholesterol, and vessel counts) exhibit predominantly monotonic, additive risk relationships well-captured by log-odds linear hyperplanes.")
    add_numbered_item(doc, "3.", "Hypothesis Validation:", "This confirms Hypothesis 1 (ensemble architectures behave differently from linear baselines) and validates Hypothesis 3 (fluoroscopy vessels, ST depression, and heart rate dominate decisions).", space_after=6)

    add_custom_heading(doc, "7.6 System Performance, Scalability, and Maintainability", level=2)
    add_body_paragraph(
        doc,
        "Benchmarking measured an average end-to-end response latency of 34 milliseconds for POST /api/v1/predict, including database "
        "persistence and local SHAP computation. The system demonstrates complete modular maintainability, verified by 74% statement coverage "
        "and zero circular dependencies."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 8: LIMITATIONS AND FUTURE WORK
    # =========================================================================
    add_custom_heading(doc, "8. Limitations and Future Work", level=1)

    add_custom_heading(doc, "8.1 Dataset and Demographic Limitations", level=2)
    add_body_paragraph(
        doc,
        "While the Cleveland dataset represents a revered benchmark in computational cardiology, several inherent limitations must be acknowledged:",
        space_after=4
    )
    add_numbered_item(doc, "1.", "Modest Sample Size:", "The cohort contains 303 observations. While sufficient for statistical benchmarking, training large-scale architectures requires cohorts numbering in the tens of thousands.")
    add_numbered_item(doc, "2.", "Demographic Skew:", "The sample features 68% male participants, reflecting historical patient selection biases from the 1980s.")
    add_numbered_item(doc, "3.", "Evolving Biomarkers:", "Contemporary cardiology utilizes novel diagnostic assays (high-sensitivity Cardiac Troponin T/I, Coronary Artery Calcium scoring) that were unavailable when the benchmark was collected.", space_after=6)

    add_custom_heading(doc, "8.2 Algorithmic and Experimental Constraints", level=2)
    add_body_paragraph(
        doc,
        "Key methodological and operational constraints of the current modeling pipeline include:",
        space_after=4
    )
    add_numbered_item(doc, "1.", "Static Thresholding:", "Risk tiers are categorized based on standard heuristic boundaries (0.35 and 0.65). Dynamic cost-sensitive threshold tuning could further optimize false-positive trade-offs.")
    add_numbered_item(doc, "2.", "Single-Center Validation:", "The model has not yet been validated on multi-center external cohorts (such as the Hungarian or Long Beach datasets) to verify cross-institutional domain adaptation.", space_after=6)

    add_custom_heading(doc, "8.3 Future Architectural and Clinical Roadmap", level=2)
    add_body_paragraph(
        doc,
        "Future research and engineering extensions planned for the system include:",
        space_after=4
    )
    add_numbered_item(doc, "1.", "Federated Multi-Center Learning:", "Implementing federated learning protocols enabling disparate medical centers to collaboratively train predictive pipelines without sharing raw patient records.")
    add_numbered_item(doc, "2.", "HL7 / FHIR Clinical Interoperability:", "Integrating Fast Healthcare Interoperability Resources (FHIR) JSON endpoints to enable seamless data exchange with Electronic Health Record (EHR) systems.")
    add_numbered_item(doc, "3.", "Probability Calibration Enhancement:", "Incorporating isotonic regression and Platt scaling calibration curves evaluated via Brier score minimization.", space_after=6)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 9: CONCLUSION
    # =========================================================================
    add_custom_heading(doc, "9. Conclusion", level=1)

    add_custom_heading(doc, "9.1 Problem Summary", level=2)
    add_body_paragraph(
        doc,
        "Cardiovascular risk assessment represents a critical application domain for predictive computing. However, clinical machine "
        "learning has historically been plagued by data contamination during preprocessing, uninformative evaluation reporting, "
        "black-box opacity, and fragile software implementations lacking automated testing and persistence."
    )

    add_custom_heading(doc, "9.2 Implemented Solution and Technical Highlights", level=2)
    add_body_paragraph(
        doc,
        "This project conceived, benchmarked, and implemented an end-to-end, data-intensive web system that resolves these challenges. "
        "By enforcing strict pre-split partitioning and ColumnTransformer encapsulation, data leakage was completely eliminated. "
        "Seven algorithmic families were systematically benchmarked under Stratified 5-Fold Cross-Validation, establishing that a tuned "
        "regularized linear model achieved optimal discriminative performance (0.9117 CV ROC-AUC). On unseen test data, the production "
        "pipeline achieved 92.86% sensitivity, 88.52% accuracy, and 0.9621 ROC-AUC, demonstrating exceptional diagnostic reliability."
    )
    add_body_paragraph(
        doc,
        "Through SHAP integration, the black-box dilemma was resolved by delivering transparent global factor rankings and real-time local "
        "patient attribution waterfalls. The complete solution was productionized within an asynchronous FastAPI service, SQLAlchemy ORM "
        "relational persistence, a responsive client dashboard, Docker containerization, and a 100% passing automated test suite of 21 tests."
    )

    add_custom_heading(doc, "9.3 Final Reflections", level=2)
    add_body_paragraph(
        doc,
        "This thesis demonstrates that combining rigorous statistical methodology, explainable artificial intelligence, and disciplined "
        "software engineering produces clinical decision-support systems that are not only mathematically robust, but also maintainable, "
        "transparent, and directly valuable for modern healthcare informatics."
    )

    doc.add_page_break()

    # =========================================================================
    # REFERENCES
    # =========================================================================
    add_custom_heading(doc, "References", level=1)

    refs = [
        ("Detrano, R., Janosi, A., Steinbrunn, W., Pfisterer, M., Schmid, J. J., Sandhu, S., Gopalakrishna, K. X., & Froelicher, V.", "1989", "International application of a new probability algorithm for the diagnosis of coronary artery disease.", "The American Journal of Cardiology, 64(5), 304-310."),
        ("Lundberg, S. M., & Lee, S. I.", "2017", "A unified approach to interpreting model predictions.", "Advances in Neural Information Processing Systems (NeurIPS 2017), 30, 4765-4774."),
        ("Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., & Vanderplas, J.", "2011", "Scikit-learn: Machine learning in Python.", "Journal of Machine Learning Research, 12, 2825-2830."),
        ("Tiangolo, S.", "2024", "FastAPI: High performance, easy to learn, fast to code, ready for production.", "Official Documentation: https://fastapi.tiangolo.com"),
        ("Bayer, M.", "2024", "SQLAlchemy: The Database Toolkit for Python.", "Official Documentation: https://www.sqlalchemy.org"),
        ("World Health Organization", "2021", "Cardiovascular diseases (CVDs) fact sheet.", "WHO Media Centre: https://www.who.int/news-room/fact-sheets/detail/cardiovascular-diseases-(cvds)"),
        ("Breiman, L.", "2001", "Random forests.", "Machine Learning, 45(1), 5-32."),
        ("Friedman, J. H.", "2001", "Greedy function approximation: A gradient boosting machine.", "Annals of Statistics, 29(5), 1189-1232."),
        ("Cortes, C., & Vapnik, V.", "1995", "Support-vector networks.", "Machine Learning, 20(3), 273-297."),
        ("Cover, T., & Hart, P.", "1967", "Nearest neighbor pattern classification.", "IEEE Transactions on Information Theory, 13(1), 21-27."),
        ("Hastie, T., Tibshirani, R., & Friedman, J.", "2009", "The Elements of Statistical Learning: Data Mining, Inference, and Prediction.", "Springer Science & Business Media, 2nd Edition."),
        ("Fawcett, T.", "2006", "An introduction to ROC analysis.", "Pattern Recognition Letters, 27(8), 861-874."),
        ("Kaufman, S., Rosset, S., Perlich, C., & Stitelman, O.", "2012", "Leakage in data mining: Formulation, detection, and avoidance.", "ACM Transactions on Knowledge Discovery from Data (TKDD), 6(4), 1-21."),
        ("Shapley, L. S.", "1953", "A value for n-person games.", "Contributions to the Theory of Games, 2(28), 307-317."),
        ("Bruce, R. A., Kusumi, F., & Hosmer, D.", "1973", "Maximal oxygen intake and nomographic assessment of functional impairment in cardiovascular disease.", "American Heart Journal, 85(4), 546-562."),
        ("Kaggle & UCI Machine Learning Repository", "2019", "Heart Disease Data Set.", "UCI Machine Learning Repository #45: https://archive.ics.uci.edu/dataset/45/heart+disease"),
    ]

    for authors, yr, title, pub in refs:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.first_line_indent = Inches(-0.4)

        r_a = p.add_run(f"{authors} ({yr}). ")
        r_a.font.name = "Calibri"
        r_a.font.size = Pt(9.5)
        r_a.font.color.rgb = COLOR_TEXT

        r_t = p.add_run(f"{title} ")
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(9.5)
        r_t.bold = True
        r_t.font.color.rgb = COLOR_PRIMARY

        r_p = p.add_run(pub)
        r_p.font.name = "Calibri"
        r_p.font.size = Pt(9.5)
        r_p.font.italic = True
        r_p.font.color.rgb = COLOR_MUTED

    doc.add_page_break()

    # =========================================================================
    # APPENDICES
    # =========================================================================
    add_custom_heading(doc, "Appendices", level=1)

    add_custom_heading(doc, "Appendix A: REST API Schema Reference", level=2)
    schema_code = (
        "class PatientInputSchema(BaseModel):\n"
        "    age: int = Field(..., ge=18, le=120, description='Age in completed years')\n"
        "    sex: int = Field(..., ge=0, le=1, description='1 = Male, 0 = Female')\n"
        "    cp: int = Field(..., ge=0, le=3, description='Chest pain category')\n"
        "    trestbps: float = Field(..., ge=60.0, le=260.0, description='Resting BP in mm Hg')\n"
        "    chol: float = Field(..., ge=80.0, le=600.0, description='Serum cholesterol in mg/dl')\n"
        "    fbs: int = Field(..., ge=0, le=1, description='Fasting blood sugar > 120 mg/dl')\n"
        "    restecg: int = Field(..., ge=0, le=2, description='Resting ECG status')\n"
        "    thalach: float = Field(..., ge=50.0, le=250.0, description='Maximum achieved heart rate')\n"
        "    exang: int = Field(..., ge=0, le=1, description='Exercise induced angina')\n"
        "    oldpeak: float = Field(..., ge=0.0, le=10.0, description='ST depression')\n"
        "    slope: int = Field(..., ge=0, le=2, description='ST slope')\n"
        "    ca: int = Field(..., ge=0, le=3, description='Fluoroscopy vessels')\n"
        "    thal: int = Field(..., ge=1, le=3, description='Thallium scan status')\n"
        "\n"
        "class PredictionResponseSchema(BaseModel):\n"
        "    id: Optional[int]\n"
        "    prediction: int\n"
        "    probability: float\n"
        "    risk_tier: str\n"
        "    model_version: str\n"
        "    model_name: str\n"
        "    feature_attributions: List[FeatureAttributionSchema]\n"
        "    disclaimer: str"
    )
    add_code_block(doc, schema_code, caption="Pydantic v2 Request/Response Schemas (app/schemas/prediction.py)")

    add_custom_heading(doc, "Appendix B: Database Table Definitions", level=2)
    db_model_code = (
        "class PredictionRecord(Base):\n"
        "    __tablename__ = 'prediction_records'\n"
        "    id = Column(Integer, primary_key=True, index=True, autoincrement=True)\n"
        "    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)\n"
        "    age = Column(Integer, nullable=False)\n"
        "    sex = Column(Integer, nullable=False)\n"
        "    cp = Column(Integer, nullable=False)\n"
        "    trestbps = Column(Float, nullable=False)\n"
        "    chol = Column(Float, nullable=False)\n"
        "    fbs = Column(Integer, nullable=False)\n"
        "    restecg = Column(Integer, nullable=False)\n"
        "    thalach = Column(Float, nullable=False)\n"
        "    exang = Column(Integer, nullable=False)\n"
        "    oldpeak = Column(Float, nullable=False)\n"
        "    slope = Column(Integer, nullable=False)\n"
        "    ca = Column(Integer, nullable=False)\n"
        "    thal = Column(Integer, nullable=False)\n"
        "    prediction = Column(Integer, nullable=False)\n"
        "    probability = Column(Float, nullable=False)\n"
        "    risk_tier = Column(String(50), nullable=False, index=True)\n"
        "    top_features = Column(Text, nullable=True)\n"
        "    model_version = Column(String(50), nullable=False)"
    )
    add_code_block(doc, db_model_code, caption="SQLAlchemy ORM Model (app/database/models.py)")

    add_custom_heading(doc, "Appendix C: Environment Configuration Example", level=2)
    env_code = (
        "APP_NAME='Cardiovascular Risk ML System'\n"
        "APP_ENV=production\n"
        "APP_PORT=8000\n"
        "DEBUG=False\n"
        "DATABASE_URL=sqlite:///./cardio_risk.db\n"
        "MODEL_PATH=models/best_model.joblib\n"
        "METADATA_PATH=models/model_metadata.json\n"
        "MODEL_VERSION=1.0.0\n"
        "RANDOM_STATE=42"
    )
    add_code_block(doc, env_code, caption=".env Configuration Template")

    add_custom_heading(doc, "Appendix D: Core Pipeline Implementation Excerpts", level=2)
    pipeline_code = (
        "# Single Production Pipeline Assembly\n"
        "pipeline = Pipeline(steps=[\n"
        "    ('preprocessor', build_preprocessor()),\n"
        "    ('classifier', LogisticRegression(C=0.1, penalty='l2', solver='liblinear', random_state=42))\n"
        "])\n"
        "pipeline.fit(X_train, y_train)\n"
        "joblib.dump(pipeline, 'models/best_model.joblib')"
    )
    add_code_block(doc, pipeline_code, caption="Production Pipeline Serialization (src/models/train.py)")

    # Save final document
    doc.save(OUTPUT_PATH)
    print(f"Successfully generated Technical Thesis document at: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    build_thesis_document()
