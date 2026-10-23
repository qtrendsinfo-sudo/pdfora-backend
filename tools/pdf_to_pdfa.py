import fitz
import os

async def run_pdf_to_pdfa(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str) -> str:
    input_path = file_paths[0]
    output_filename = f"{orig_filename}_pdfa_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    doc = fitz.open(input_path)
    doc.save(output_path, garbage=4, deflate=True, pdfa=True)
    doc.close()
    return output_path
