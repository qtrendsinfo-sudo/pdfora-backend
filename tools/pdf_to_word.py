import os
from pdf2docx import Converter

async def run_pdf_to_word(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str) -> str:
    input_path = file_paths[0]
    output_filename = f"{orig_filename}_{unique_suffix}.docx"
    output_path = os.path.join(temp_dir, output_filename)
    
    cv = Converter(input_path)
    cv.convert(output_path, start=0, end=None)
    cv.close()
    
    return output_path
