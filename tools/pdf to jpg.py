import os
import fitz
import zipfile
import uuid

async def run_pdf_to_jpg(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str) -> str:
    input_path = file_paths[0]
    zip_name = f"{orig_filename}_images_{unique_suffix}.zip"
    zip_path = os.path.join(temp_dir, zip_name)
    
    doc = fitz.open(input_path)
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for i, page in enumerate(doc):
            pix = page.get_pixmap()
            img_name = f"page_{i+1}.jpg"
            img_path = os.path.join(temp_dir, f"{uuid.uuid4().hex[:6]}_{img_name}")
            pix.save(img_path)
            zf.write(img_path, arcname=img_name)
            os.remove(img_path)
            
    doc.close()
    return zip_path
