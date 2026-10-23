import fitz
import os

async def run_unlock_pdf(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str, extra_param: str = None) -> str:
    input_path = file_paths[0]
    output_filename = f"{orig_filename}_unlocked_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    doc = fitz.open(input_path)
    if doc.is_encrypted:
        password = extra_param if extra_param else ""
        doc.authenticate(password)
        
    doc.save(output_path)
    doc.close()
    return output_path
