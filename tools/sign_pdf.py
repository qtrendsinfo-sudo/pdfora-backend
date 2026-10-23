import fitz
import os

async def run_sign_pdf(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str, extra_param: str = None) -> str:
    input_path = file_paths[0]
    output_filename = f"{orig_filename}_signed_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    doc = fitz.open(input_path)
    sign_text = extra_param if extra_param else "Digitally Signed"
    
    if len(doc) > 0:
        page = doc[-1]
        rect = fitz.Rect(400, 700, 550, 750)
        page.insert_textbox(rect, sign_text, fontsize=12, color=(0, 0, 1))
        
    doc.save(output_path)
    doc.close()
    return output_path
