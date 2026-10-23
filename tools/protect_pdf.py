import fitz
import os

async def run_protect_pdf(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str, extra_param: str = None) -> str:
    input_path = file_paths[0]
    output_filename = f"{orig_filename}_protected_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    doc = fitz.open(input_path)
    password = extra_param if extra_param else "12345"
    
    doc.save(
        output_path,
        encryption=fitz.PDF_ENCRYPT_AES_240,
        owner_pw=password,
        user_pw=password,
        permissions=fitz.PDF_PERM_ACCESSIBILITY | fitz.PDF_PERM_PRINT
    )
    doc.close()
    return output_path
