from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
import time
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
async def process_pdf(tool_name: str = Form(...), file: UploadFile = File(...)):
    local_path = None
    output_path = None
    try:
        safe_filename = "".join([c for c in file.filename if c.isalnum() or c in ('_', '-', '.')])
        local_path = os.path.join(TEMP_DIR, safe_filename)
        with open(local_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        timestamp_str = str(int(time.time()))
        # Strict clean filename to prevent Supabase InvalidKey error
        output_filename = f"processed_{timestamp_str}.pdf"
        output_path = os.path.join(TEMP_DIR, output_filename)
        
        tool = tool_name.lower().strip()
        ext = safe_filename.lower()
        
        if "jpg" in tool or "png" in tool or "image" in tool or ext.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            c = canvas.Canvas(output_path, pagesize=letter)
            page_width, page_height = letter
            c.drawImage(local_path, 50, 50, width=page_width-100, height=page_height-100, preserveAspectRatio=True, anchor='c')
            c.showPage()
            c.save()
        else:
            reader = PdfReader(local_path)
            writer = PdfWriter()
            
            if "rotate" in tool:
                for page in reader.pages:
                    page.rotate(90)
                    writer.add_page(page)
                with open(output_path, "wb") as f:
                    writer.write(f)
                    
            elif "split" in tool or "remove pages" in tool:
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
                with open(output_path, "wb") as f:
                    writer.write(f)
                    
            else:
                shutil.copy(local_path, output_path)
            
        with open(output_path, "rb") as f:
            file_bytes = f.read()
            
        supabase.storage.from_(BUCKET_NAME.strip()).upload(
            path=output_filename,
            file=file_bytes,
            file_options={"content-type": "application/pdf", "upsert": "true"}
        )
            
        res = supabase.storage.from_(BUCKET_NAME.strip()).get_public_url(output_filename)
        
        if isinstance(res, dict):
            public_url = res.get("publicUrl") or res.get("data", {}).get("publicUrl") or str(res)
        else:
            public_url = str(res)
        
        return {
            "status": "success",
            "tool": tool_name,
            "download_url": public_url
        }
        
    except Exception as e:
        print(f"Backend Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        if local_path and os.path.exists(local_path):
            try: os.remove(local_path)
            except: pass
        if output_path and os.path.exists(output_path):
            try: os.remove(output_path)
            except: pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
