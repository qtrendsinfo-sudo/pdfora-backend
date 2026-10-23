import os
import fitz

async def run_jpg_to_pdf(file_paths: list[str], temp_dir: str, orig_filename: str, unique_suffix: str) -> str:
    output_filename = f"{orig_filename}_converted_{unique_suffix}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    doc = fitz.open()
    for path in file_paths:
        img_doc = fitz.open(path)
        pdfbytes = img_doc.convert_to_pdf()
        img_pdf = fitz.open("pdf", pdfbytes)
        doc.insert_pdf(img_pdf)
        img_doc.close()
        img_pdf.close()
        
    doc.save(output_path)
    doc.close()
    return output_path
