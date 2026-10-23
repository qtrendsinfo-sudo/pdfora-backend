import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

async def run_excel_to_pdf(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str) -> str:
    input_path = file_paths[0]
    output_filename = f"{orig_filename}_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    df = pd.read_excel(input_path)
    pdf_doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    for index, row in df.iterrows():
        row_str = " | ".join([str(val) for val in row.values if pd.notna(val)])
        if row_str.strip():
            story.append(Paragraph(row_str, styles['Normal']))
            story.append(Spacer(1, 6))
            
    pdf_doc.build(story)
    return output_path
