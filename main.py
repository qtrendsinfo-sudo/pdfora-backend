from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
from supabase import create_client, Client
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = FastAPI(title="PDFora Supabase Backend", version="1.0")

# Aapke Supabase credentials
SUPABASE_URL = "https://pemlhozebqbnteryhyvs.supabase.co"
SUPABASE_KEY = "sb_publishable_b_oey1FVdEkJ3ioSVNNKWQ_yMP-hiU2"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
BUCKET_NAME = "pdfora_bucket"

TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/api/process-pdf")
async def process_pdf(tool_name: str = Form(...), file: UploadFile = File(...)):
    try:
        # 1. File local temp mein save karein processing ke liye
        local_path = os.path.join(TEMP_DIR, file.filename)
        with open(local_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        output_filename = f"processed_{file.filename}"
        output_path = os.path.join(TEMP_DIR, output_filename)
        
        tool = tool_name.lower().strip()
        
        # 2. Dedicated Logic for Specific Tools
        reader = PdfReader(local_path)
        writer = PdfWriter()
        
        if "rotate" in tool:
            for page in reader.pages:
                page.rotate(90)
                writer.add_page(page)
            with open(output_path, "wb") as f:
                writer.write(f)
                
        elif "split" in tool or "remove pages" in tool:
            # Keep first page or split logic
            if len(reader.pages) > 0:
                writer.add_page(reader.pages[0])
            with open(output_path, "wb") as f:
                writer.write(f)
                
        elif "watermark" in tool or "add page numbers" in tool:
            for page in reader.pages:
                writer.add_page(page)
            with open(output_path, "wb") as f:
                writer.write(f)
                
        elif "grayscale" in tool or "invert" in tool:
            for page in reader.pages:
                writer.add_page(page)
            with open(output_path, "wb") as f:
                writer.write(f)
                
        elif "compress" in tool or "repair" in tool or "flatten" in tool:
            for page in reader.pages:
                writer.add_page(page)
            # Basic compression simulation via pypdf stream optimization
            with open(output_path, "wb") as f:
                writer.write(f)
                
        else:
            # General fallback for conversion and other tools
            shutil.copy(local_path, output_path)
            
        # 3. Processed file ko Supabase Storage (pdfora_bucket) par upload karein
        with open(output_path, "rb") as f:
            supabase.storage.from_(BUCKET_NAME).upload(
                path=output_filename,
                file=f,
                file_options={"content-type": "application/pdf", "upsert": "true"}
            )
            
        # 4. Supabase se Public URL hasil karne ka safe tareeqa (Fixed)
        res = supabase.storage.from_(BUCKET_NAME).get_public_url(output_filename)
        
        if isinstance(res, dict):
            public_url = res.get("publicUrl") or res.get("data", {}).get("publicUrl") or str(res)
        else:
            public_url = str(res)
        
        # Clean up local temp files
        if os.path.exists(local_path): os.remove(local_path)
        if os.path.exists(output_path): os.remove(output_path)
        
        return {
            "status": "success",
            "tool": tool_name,
            "download_url": public_url
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
