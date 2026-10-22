from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import List
import os
import shutil
import time
import uuid
from supabase import create_client, Client
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = FastAPI(title="PDFora Supabase Backend", version="1.0")

SUPABASE_URL = "https://pemlhozebqbnteryhyvs.supabase.co"
SUPABASE_KEY = "sb_publishable_b_oey1FVdEkJ3ioSVNNKWQ_yMP-hiU2"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
BUCKET_NAME = "pdfora_bucket"

TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/api/process-pdf")
async def process_pdf(tool_name: str = Form(...), file: List[UploadFile] = File(...)):
    local_paths = []
    output_path = None
    try:
        tool = tool_name.lower().strip()
        timestamp_str = str(int(time.time()))
        unique_suffix = uuid.uuid4().hex[:6]
        
        # Tool ke lehaz se exact output extension set karna
        out_ext = ".pdf"
        if "to jpg" in tool or "to image" in tool or "jpg" in tool:
            out_ext = ".jpg"
        elif "to word" in tool or "docx" in tool:
            out_ext = ".docx"
        elif "to excel" in tool or "xlsx" in tool:
            out_ext = ".xlsx"
        elif "to ppt" in tool or "pptx" in tool:
            out_ext = ".pptx"
        elif "extract images" in tool or "split" in tool:
            out_ext = ".zip"
        elif "merge" in tool or "pdf" in tool:
            out_ext = ".pdf"
            
        output_filename = f"processed_{timestamp_str}_{unique_suffix}{out_ext}"
        output_path = os.path.join(TEMP_DIR, output_filename)
        
        # 1. Merge Tool Logic (Multiple files handling)
        if "merge" in tool and len(file) > 0:
            writer = PdfWriter()
            for f in file:
                orig_name = f.filename or "doc.pdf"
                ext = os.path.splitext(orig_name)[1].lower() or ".pdf"
                temp_p = os.path.join(TEMP_DIR, f"in_{uuid.uuid4().hex[:6]}{ext}")
                with open(temp_p, "wb") as buffer:
                    shutil.copyfileobj(f.file, buffer)
                local_paths.append(temp_p)
                
                try:
                    reader = PdfReader(temp_p)
                    for page in reader.pages:
                        writer.add_page(page)
                except Exception:
                    pass
                    
            with open(output_path, "wb") as f:
                writer.write(f)
        else:
            # Single file handling
            single_file = file[0]
            orig_name = single_file.filename or "document.pdf"
            ext = os.path.splitext(orig_name)[1].lower() or ".pdf"
            temp_p = os.path.join(TEMP_DIR, f"single_{uuid.uuid4().hex[:6]}{ext}")
            local_paths.append(temp_p)
            
            with open(temp_p, "wb") as buffer:
                shutil.copyfileobj(single_file.file, buffer)
                
            if ext in ['.jpg', '.jpeg', '.png', '.webp'] and ("jpg" in tool or "png" in tool or "image" in tool):
                c = canvas.Canvas(output_path, pagesize=letter)
                pw, ph = letter
                c.drawImage(temp_p, 50, 50, width=pw-100, height=ph-100, preserveAspectRatio=True, anchor='c')
                c.showPage()
                c.save()
            elif "rotate" in tool:
                reader = PdfReader(temp_p)
                writer = PdfWriter()
                for page in reader.pages:
                    page.rotate(90)
                    writer.add_page(page)
                with open(output_path, "wb") as f:
                    writer.write(f)
            else:
                shutil.copy(temp_p, output_path)
                
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            if local_paths:
                shutil.copy(local_paths[0], output_path)

        # Supabase Upload with correct content-type
        with open(output_path, "rb") as f:
            file_bytes = f.read()
            
        content_type = "application/pdf"
        if out_ext == ".jpg": 
            content_type = "image/jpeg"
        elif out_ext == ".docx": 
            content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        elif out_ext == ".xlsx":
            content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif out_ext == ".zip": 
            content_type = "application/zip"
        
        supabase.storage.from_(BUCKET_NAME.strip()).upload(
            path=output_filename,
            file=file_bytes,
            file_options={"content-type": content_type, "upsert": "true"}
        )
            
        res = supabase.storage.from_(BUCKET_NAME.strip()).get_public_url(output_filename)
        public_url = res.get("publicUrl") if isinstance(res, dict) else str(res)
        
        return {
            "status": "success",
            "tool": tool_name,
            "download_url": public_url
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        for p in local_paths:
            if p and os.path.exists(p):
                try: os.remove(p)
                except: pass
        if output_path and os.path.exists(output_path):
            try: os.remove(output_path)
            except: pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
