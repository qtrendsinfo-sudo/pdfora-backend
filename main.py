from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import List
import os
import shutil
import time
import uuid
from supabase import create_client, Client
from pypdf import PdfReader, PdfWriter
import fitz  # PyMuPDF for robust PDF processing

app = FastAPI(title="PDFora Supabase Backend", version="1.0")

SUPABASE_URL = "https://pemlhozebqbnteryhyvs.supabase.co"
SUPABASE_KEY = "sb_publishable_b_oey1FVdEkJ3ioSVNNKWQ_yMP-hiU2"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
BUCKET_NAME = "pdfora_bucket"

TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/api/process-pdf")
async def process_pdf(
    tool_name: str = Form(...), 
    file: List[UploadFile] = File(...),
    extra_param: str = Form(None)
):
    local_paths = []
    output_path = None
    try:
        tool = tool_name.lower().strip()
        timestamp_str = str(int(time.time()))
        unique_suffix = uuid.uuid4().hex[:6]
        
        # Original file ka naam nikalna taake output mein wahi use ho
        orig_filename = "document"
        if len(file) > 0 and file[0].filename:
            orig_filename = os.path.splitext(file[0].filename)[0]
        
        out_ext = ".pdf"
        if "to jpg" in tool or "to image" in tool:
            out_ext = ".jpg"
        elif "to word" in tool:
            out_ext = ".docx"
        elif "to excel" in tool:
            out_ext = ".xlsx"
        elif "split" in tool or "extract" in tool:
            out_ext = ".zip"
            
        tool_tag = tool.replace(" ", "_")
        output_filename = f"{orig_filename}_{tool_tag}_{unique_suffix}{out_ext}"
        output_path = os.path.join(TEMP_DIR, output_filename)
        
        # 1. Merge PDF
        if "merge" in tool and len(file) > 0:
            writer = PdfWriter()
            for f in file:
                temp_p = os.path.join(TEMP_DIR, f"in_{uuid.uuid4().hex[:6]}.pdf")
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
            single_file = file[0]
            temp_p = os.path.join(TEMP_DIR, f"single_{uuid.uuid4().hex[:6]}.pdf")
            local_paths.append(temp_p)
            with open(temp_p, "wb") as buffer:
                shutil.copyfileobj(single_file.file, buffer)
                
            # 2. Rotate PDF using PyMuPDF
            if "rotate" in tool:
                doc = fitz.open(temp_p)
                for page in doc:
                    rot = page.rotation
                    page.set_rotation((rot + 90) % 360)
                doc.save(output_path)
                doc.close()
                
            # 3. Compress PDF
            elif "compress" in tool:
                doc = fitz.open(temp_p)
                doc.save(output_path, garbage=4, deflate=True)
                doc.close()
                
            # 4. Remove / Extract Pages or Organize
            elif "remove" in tool or "extract" in tool or "organize" in tool:
                doc = fitz.open(temp_p)
                writer = PdfWriter()
                reader = PdfReader(temp_p)
                for page in reader.pages:
                    writer.add_page(page)
                with open(output_path, "wb") as f:
                    writer.write(f)
                doc.close()
                
            # 5. Fallback copy
            else:
                shutil.copy(temp_p, output_path)
                
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            if local_paths:
                shutil.copy(local_paths[0], output_path)

        with open(output_path, "rb") as f:
            file_bytes = f.read()
            
        supabase.storage.from_(BUCKET_NAME.strip()).upload(
            path=output_filename,
            file=file_bytes,
            file_options={"content-type": "application/pdf", "upsert": "true"}
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
    # Render ke dynamic PORT environment variable ko uthane ke liye updated configuration:
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
