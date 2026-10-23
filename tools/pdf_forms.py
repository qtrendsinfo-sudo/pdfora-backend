import fitz
import os

async def run_pdf_forms(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str, extra_param: str = None) -> str:
    input_path = file_paths[0]
    output_filename = f"{orig_filename}_form_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    doc = fitz.open(input_path)
    
    # Interactive form fields fill karne ke liye logic
    for page in doc:
        for widget in page.widgets():
            if extra_param and "=" in extra_param:
                parts = extra_param.split("=")
                if len(parts) == 2 and widget.field_name == parts[0].strip():
                    widget.field_value = parts[1].strip()
                    widget.update()
                    
    doc.save(output_path)
    doc.close()
    return output_path
