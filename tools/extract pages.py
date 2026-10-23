import fitz
import os

async def run_extract_pages(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str, extra_param: str = None) -> str:
    input_path = file_paths[0]
    output_filename = f"{orig_filename}_extracted_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    doc = fitz.open(input_path)
    new_doc = fitz.open()
    
    if extra_param:
        try:
            pages_to_extract = [int(p.strip()) for p in extra_param.split(",") if p.strip().isdigit()]
            for pno in pages_to_extract:
                if 0 <= pno < len(doc):
                    new_doc.insert_pdf(doc, from_page=pno, to_page=pno)
        except Exception:
            new_doc.insert_pdf(doc)
    else:
        new_doc.insert_pdf(doc)
        
    new_doc.save(output_path)
    new_doc.close()
    doc.close()
    return output_path
