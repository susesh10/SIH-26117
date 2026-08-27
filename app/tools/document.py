from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
import os

def create_approval_note(content: str, output_folder: str = "outputs") -> str:
    """
    Creates a properly formatted Word document from the approval note content.
    Returns the path of the generated file.
    """
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Create document
    doc = Document()

    # Set narrow margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # ---- Title ----
    title = doc.add_heading("Inspection Observation / Approval Note", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # ---- Date & Reference ----
    date_para = doc.add_paragraph()
    date_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = date_para.add_run(f"Date: {datetime.now().strftime('%d %B %Y')}")
    run.bold = True

    # ---- Main Content ----
    # Split the content coming from the model into paragraphs
    for line in content.split("\n"):
        line = line.strip()
        if not line:
            continue

        # Make headings bold
        if line.startswith("**") and line.endswith("**"):
            clean_line = line.replace("**", "")
            heading = doc.add_heading(clean_line, level=2)
        elif line.startswith("Title:") or line.startswith("Date:") or line.startswith("Reference:"):
            para = doc.add_paragraph()
            run = para.add_run(line)
            run.bold = True
        else:
            doc.add_paragraph(line)

    # ---- Signature Section ----
    doc.add_paragraph("\n")
    doc.add_paragraph("Prepared by: ___________________________")
    doc.add_paragraph("Designation: Inspection Engineer")
    doc.add_paragraph("\n")
    doc.add_paragraph("Approved by: ___________________________")
    doc.add_paragraph("Designation: Head of Maintenance / Section Head")

    # ---- Save File ----
    filename = f"Approval_Note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    filepath = os.path.join(output_folder, filename)
    doc.save(filepath)

    return filepath