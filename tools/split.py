import os
import zipfile
from pypdf import PdfReader, PdfWriter

async def run_split(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str, extra_param: str = None) -> str:
    input_path = file_paths[0]
    reader = PdfReader(input_path)
    zip_name = f"{orig_filename}_split_{unique_suffix}.zip"
    zip_path = os.path.join(temp_dir, zip_name)
    
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            part_name = f"{orig_filename}_page_{i+1}.pdf"
            part_path = os.path.join(temp_dir, part_name)
            with open(part_path, "wb") as f:
                writer.write(f)
            zf.write(part_path, arcname=part_name)
            os.remove(part_path)
            
    return zip_path
