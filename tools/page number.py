import fitz
import os

async def run_page_number(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str, extra_param: str = None) -> str:
    input_path = file_paths[0]
    output_filename = f"{orig_filename}_numbered_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    doc = fitz.open(input_path)
    total_pages = len(doc)
    
    for i, page in enumerate(doc):
        rect = page.rect
        text = f"Page {i+1} of {total_pages}"
        point = fitz.Point(rect.width / 2 - 30, rect.height - 30)
        page.insert_text(point, text, fontsize=10, color=(0.2, 0.2, 0.2))
        
    doc.save(output_path)
    doc.close()
    return output_path
