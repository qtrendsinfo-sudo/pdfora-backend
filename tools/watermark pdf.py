import fitz
import os

async def run_watermark_pdf(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str, extra_param: str = None) -> str:
    input_path = file_paths[0]
    output_filename = f"{orig_filename}_watermarked_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    doc = fitz.open(input_path)
    watermark_text = extra_param if extra_param else "CONFIDENTIAL"
    
    for page in doc:
        rect = page.rect
        point = fitz.Point(rect.width / 4, rect.height / 2)
        page.insert_text(point, watermark_text, fontsize=36, color=(0.7, 0.7, 0.7), rotate=45)
        
    doc.save(output_path)
    doc.close()
    return output_path
