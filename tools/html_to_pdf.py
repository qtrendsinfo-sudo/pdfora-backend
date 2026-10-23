import os
import pdfkit
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

async def run_html_to_pdf(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str, extra_param: str = None) -> str:
    output_filename = f"{orig_filename}_html_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    html_content = extra_param if extra_param else "<h1>PDFora HTML Document</h1><p>Converted successfully.</p>"
    
    pdf_doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [Paragraph(html_content, styles['Normal'])]
    
    pdf_doc.build(story)
    return output_path
