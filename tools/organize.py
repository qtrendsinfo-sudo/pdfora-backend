import fitz
import os

async def run_organize(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str, extra_param: str = None) -> str:
    input_path = file_paths[0]
    output_filename = f"{orig_filename}_organized_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    doc = fitz.open(input_path)
    # Organize logic (default pass-through or reorder if parameters provided)
    doc.save(output_path)
    doc.close()
    
    return output_path
