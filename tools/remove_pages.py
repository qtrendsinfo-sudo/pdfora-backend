import fitz
import os

async def run_remove_pages(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str, extra_param: str = None) -> str:
    input_path = file_paths[0]
    output_filename = f"{orig_filename}_pages_removed_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    doc = fitz.open(input_path)
    # extra_param format e.g. "0,1" (zero-based index pages to delete)
    if extra_param:
        try:
            pages_to_remove = [int(p.strip()) for p in extra_param.split(",") if p.strip().isdigit()]
            doc.delete_pages(pages_to_remove)
        except Exception:
            pass
            
    doc.save(output_path)
    doc.close()
    return output_path
