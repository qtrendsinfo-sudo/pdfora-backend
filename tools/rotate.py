import fitz
import os

async def run_rotate(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str, extra_param: str = None) -> str:
    input_path = file_paths[0]
    output_filename = f"{orig_filename}_rotated_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    doc = fitz.open(input_path)
    rotation_angle = int(extra_param) if extra_param and extra_param.isdigit() else 90
    
    for page in doc:
        rot = page.rotation
        page.set_rotation((rot + rotation_angle) % 360)
        
    doc.save(output_path)
    doc.close()
    
    return output_path
