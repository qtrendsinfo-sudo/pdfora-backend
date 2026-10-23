import os
import pdfplumber
import pandas as pd

async def run_pdf_to_excel(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str) -> str:
    input_path = file_paths[0]
    output_filename = f"{orig_filename}_{unique_suffix}.xlsx"
    output_path = os.path.join(temp_dir, output_filename)
    
    all_data = []
    with pdfplumber.open(input_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    all_data.append(row)
                    
    df = pd.DataFrame(all_data)
    df.to_excel(output_path, index=False, header=False)
    
    return output_path
