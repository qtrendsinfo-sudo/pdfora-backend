import os
import fitz
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from docx import Document

async def run_word_to_pdf(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str) -> str:
    input_path = file_paths[0]
    output_filename = f"{orig_filename}_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    doc_docx = Document(input_path)
    pdf_doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    for para in doc_docx.paragraphs:
        if para.text.strip():
            story.append(Paragraph(para.text, styles['Normal']))
            story.append(Spacer(1, 10))
            
    pdf_doc.build(story)
    return output_path
