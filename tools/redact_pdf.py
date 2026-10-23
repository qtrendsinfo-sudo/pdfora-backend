import fitz
import os

async def run_redact_pdf(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str, extra_param: str = None) -> str:
    input_path = file_paths[0]
    output_filename = f"{orig_filename}_redacted_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    doc = fitz.open(input_path)
    search_text = extra_param if extra_param else "Confidential"
    
    for page in doc:
        areas = page.search_for(search_text)
        for rect in areas:
            page.add_redact_annot(rect, fill=(0, 0, 0))
        page.apply_redactions()
        
    doc.save(output_path)
    doc.close()
    return output_path
