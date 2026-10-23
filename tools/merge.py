import fitz
import os

async def run_merge(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str) -> str:
    doc_out = fitz.open()
    for path in file_paths:
        with fitz.open(path) as doc_in:
            doc_out.insert_pdf(doc_in)
    
    output_filename = f"{orig_filename}_merged_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    doc_out.save(output_path)
    doc_out.close()
    return output_path
