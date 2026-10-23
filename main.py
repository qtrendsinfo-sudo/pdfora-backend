from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import List
import os
import shutil
import time
import uuid
from supabase import create_client, Client

# Import all tools from tools folder (extract_txt removed, pdf_forms added)
from tools.merge import run_merge
from tools.split import run_split
from tools.compress import run_compress
from tools.rotate import run_rotate
from tools.organize import run_organize
from tools.remove_pages import run_remove_pages
from tools.extract_pages import run_extract_pages
from tools.pdf_to_word import run_pdf_to_word
from tools.word_to_pdf import run_word_to_pdf
from tools.pdf_to_excel import run_pdf_to_excel
from tools.excel_to_pdf import run_excel_to_pdf
from tools.pdf_to_ppt import run_pdf_to_ppt
from tools.ppt_to_pdf import run_ppt_to_pdf
from tools.pdf_to_jpg import run_pdf_to_jpg
from tools.jpg_to_pdf import run_jpg_to_pdf
from tools.edit_pdf import run_edit_pdf
from tools.ocr_pdf import run_ocr_pdf
from tools.watermark_pdf import run_watermark_pdf
from tools.page_number import run_page_number
from tools.unlock_pdf import run_unlock_pdf
from tools.protect_pdf import run_protect_pdf
from tools.repair_pdf import run_repair_pdf
from tools.sign_pdf import run_sign_pdf
from tools.pdf_to_pdfa import run_pdf_to_pdfa
from tools.compare_pdf import run_compare_pdf
from tools.crop_pdf import run_crop_pdf
from tools.redact_pdf import run_redact_pdf
from tools.html_to_pdf import run_html_to_pdf
from tools.scan_to_pdf import run_scan_to_pdf
from tools.pdf_forms import run_pdf_forms

app = FastAPI(title="PDFora Backend Master Router", version="2.0")

SUPABASE_URL = "https://pemlhozebqbnteryhyvs.supabase.co"
SUPABASE_KEY = "sb_publishable_b_oey1FVdEkJ3ioSVNNKWQ_yMP-hiU2"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
BUCKET_NAME = "pdfora_bucket"

TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"status": "PDFora Backend Router Active", "tools_count": 30}

@app.post("/api/process-pdf")
async def process_pdf(
    tool_name: str = Form(...), 
    file: List[UploadFile] = File(...),
    extra_param: str = Form(None)
):
    local_input_paths = []
    output_path = None
    try:
        tool = tool_name.lower().strip()
        unique_suffix = uuid.uuid4().hex[:6]
        
        # Save uploaded files locally
        for f in file:
            temp_p = os.path.join(TEMP_DIR, f"in_{uuid.uuid4().hex[:6]}_{f.filename}")
            with open(temp_p, "wb") as buffer:
                shutil.copyfileobj(f.file, buffer)
            local_input_paths.append(temp_p)

        orig_filename = "document"
        if len(file) > 0 and file[0].filename:
            orig_filename = os.path.splitext(file[0].filename)[0]

        # Route dynamically to specific tool file
        if tool == "merge.py" or tool == "merge":
            output_path = await run_merge(local_input_paths, TEMP_DIR, orig_filename, unique_suffix)
        elif tool == "split.py" or tool == "split":
            output_path = await run_split(local_input_paths, TEMP_DIR, orig_filename, unique_suffix, extra_param)
        elif tool == "compress.py" or tool == "compress":
            output_path = await run_compress(local_input_paths, TEMP_DIR, orig_filename, unique_suffix)
        elif tool == "rotate.py" or tool == "rotate":
            output_path = await run_rotate(local_input_paths, TEMP_DIR, orig_filename, unique_suffix, extra_param)
        elif tool == "organize.py" or tool == "organize":
            output_path = await run_organize(local_input_paths, TEMP_DIR, orig_filename, unique_suffix, extra_param)
        elif tool == "remove pages.py" or tool == "remove_pages":
            output_path = await run_remove_pages(local_input_paths, TEMP_DIR, orig_filename, unique_suffix, extra_param)
        elif tool == "extract pages.py" or tool == "extract_pages":
            output_path = await run_extract_pages(local_input_paths, TEMP_DIR, orig_filename, unique_suffix, extra_param)
        elif tool == "pdf to word.py" or tool == "pdf_to_word":
            output_path = await run_pdf_to_word(local_input_paths, TEMP_DIR, orig_filename, unique_suffix)
        elif tool == "word to pdf.py" or tool == "word_to_pdf":
            output_path = await run_word_to_pdf(local_input_paths, TEMP_DIR, orig_filename, unique_suffix)
        elif tool == "pdf to excel.py" or tool == "pdf_to_excel":
            output_path = await run_pdf_to_excel(local_input_paths, TEMP_DIR, orig_filename, unique_suffix)
        elif tool == "excel to pdf.py" or tool == "excel_to_pdf":
            output_path = await run_excel_to_pdf(local_input_paths, TEMP_DIR, orig_filename, unique_suffix)
        elif tool == "pdf to ppt.py" or tool == "pdf_to_ppt":
            output_path = await run_pdf_to_ppt(local_input_paths, TEMP_DIR, orig_filename, unique_suffix)
        elif tool == "ppt to pdf.py" or tool == "ppt_to_pdf":
            output_path = await run_ppt_to_pdf(local_input_paths, TEMP_DIR, orig_filename, unique_suffix)
        elif tool == "pdf to jpg.py" or tool == "pdf_to_jpg":
            output_path = await run_pdf_to_jpg(local_input_paths, TEMP_DIR, orig_filename, unique_suffix)
        elif tool == "jpg to pdf.py" or tool == "jpg_to_pdf":
            output_path = await run_jpg_to_pdf(local_input_paths, TEMP_DIR, orig_filename, unique_suffix)
        elif tool == "edit pdf.py" or tool == "edit_pdf":
            output_path = await run_edit_pdf(local_input_paths, TEMP_DIR, orig_filename, unique_suffix, extra_param)
        elif tool == "ocr pdf.py" or tool == "ocr_pdf":
            output_path = await run_ocr_pdf(local_input_paths, TEMP_DIR, orig_filename, unique_suffix)
        elif tool == "watermark pdf.py" or tool == "watermark_pdf":
            output_path = await run_watermark_pdf(local_input_paths, TEMP_DIR, orig_filename, unique_suffix, extra_param)
        elif tool == "page number.py" or tool == "page_number":
            output_path = await run_page_number(local_input_paths, TEMP_DIR, orig_filename, unique_suffix, extra_param)
        elif tool == "unlock pdf.py" or tool == "unlock_pdf":
            output_path = await run_unlock_pdf(local_input_paths, TEMP_DIR, orig_filename, unique_suffix, extra_param)
        elif tool == "protect pdf.py" or tool == "protect_pdf":
            output_path = await run_protect_pdf(local_input_paths, TEMP_DIR, orig_filename, unique_suffix, extra_param)
        elif tool == "repair pdf.py" or tool == "repair_pdf":
            output_path = await run_repair_pdf(local_input_paths, TEMP_DIR, orig_filename, unique_suffix)
        elif tool == "sign pdf.py" or tool == "sign_pdf":
            output_path = await run_sign_pdf(local_input_paths, TEMP_DIR, orig_filename, unique_suffix, extra_param)
        elif tool == "pdf to pdfa.py" or tool == "pdf_to_pdfa":
            output_path = await run_pdf_to_pdfa(local_input_paths, TEMP_DIR, orig_filename, unique_suffix)
        elif tool == "compare pdf.py" or tool == "compare_pdf":
            output_path = await run_compare_pdf(local_input_paths, TEMP_DIR, orig_filename, unique_suffix)
        elif tool == "crop pdf.py" or tool == "crop_pdf":
            output_path = await run_crop_pdf(local_input_paths, TEMP_DIR, orig_filename, unique_suffix, extra_param)
        elif tool == "redact pdf.py" or tool == "redact_pdf":
            output_path = await run_redact_pdf(local_input_paths, TEMP_DIR, orig_filename, unique_suffix, extra_param)
        elif tool == "html to pdf.py" or tool == "html_to_pdf":
            output_path = await run_html_to_pdf(local_input_paths, TEMP_DIR, orig_filename, unique_suffix, extra_param)
        elif tool == "scan to pdf.py" or tool == "scan_to_pdf":
            output_path = await run_scan_to_pdf(local_input_paths, TEMP_DIR, orig_filename, unique_suffix)
        elif tool == "pdf forms.py" or tool == "pdf_forms" or tool == "pdf forms":
            output_path = await run_pdf_forms(local_input_paths, TEMP_DIR, orig_filename, unique_suffix, extra_param)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported tool name: {tool_name}")

        # Supabase Upload Logic
        output_filename = os.path.basename(output_path)
        with open(output_path, "rb") as f:
            file_bytes = f.read()

        mime_type = "application/pdf"
        if output_filename.endswith(".zip"):
            mime_type = "application/zip"
        elif output_filename.endswith(".docx"):
            mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        elif output_filename.endswith(".xlsx"):
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif output_filename.endswith(".jpg"):
            mime_type = "image/jpeg"
        elif output_filename.endswith(".txt"):
            mime_type = "text/plain"

        supabase.storage.from_(BUCKET_NAME.strip()).upload(
            path=output_filename,
            file=file_bytes,
            file_options={"content-type": mime_type, "upsert": "true"}
        )

        res = supabase.storage.from_(BUCKET_NAME.strip()).get_public_url(output_filename)
        public_url = res.get("publicUrl") if isinstance(res, dict) else str(res)

        return {
            "status": "success",
            "tool": tool_name,
            "download_url": public_url
        }

    except Exception as e:
        print(f"Error in processing {tool_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Local cleanup
        for p in local_input_paths:
            if p and os.path.exists(p):
                try: os.remove(p)
                except: pass
        if output_path and os.path.exists(output_path):
            try: os.remove(output_path)
            except: pass

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
