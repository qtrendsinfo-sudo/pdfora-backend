import fitz
import os

async def run_crop_pdf(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str, extra_param: str = None) -> str:
    input_path = file_paths[0]
    output_filename = f"{orig_filename}_cropped_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    doc = fitz.open(input_path)
    for page in doc:
        rect = page.rect
        # Margin crop karna (e.g. 36 points charo taraf se)
        new_rect = fitz.Rect(rect.x0 + 20, rect.y0 + 20, rect.x1 - 20, rect.y1 - 20)
        page.set_cropbox(new_rect)
        
    doc.save(output_path)
    doc.close()
    return output_path
