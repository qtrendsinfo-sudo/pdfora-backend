import fitz
import os

async def run_edit_pdf(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str, extra_param: str = None) -> str:
    input_path = file_paths[0]
    output_filename = f"{orig_filename}_edited_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    doc = fitz.open(input_path)
    if extra_param and len(doc) > 0:
        page = doc[0]
        page.insert_text((50, 50), extra_param, fontsize=12, color=(1, 0, 0))
        
    doc.save(output_path)
    doc.close()
    return output_path
