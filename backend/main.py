import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
 
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
 
from ocr.extract import extract_text_from_image, clean_text_with_mojo
from models.analyze import extract_findings, explain_finding
 
app = FastAPI()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
 
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
 
 
@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))
 
 
@app.get("/health")
def health_check():
    return {"status": "ok"}
 
 
@app.post("/upload-report")
async def upload_report(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Only PNG/JPG images are supported")
 
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
 
        text = extract_text_from_image(file_path)
        text = clean_text_with_mojo(text)
        findings = extract_findings(text)
 
        results = []
        for finding in findings:
            explanation = explain_finding(finding["test_name"], finding["value"], finding["unit"])
            finding["simple_explanation"] = explanation
            results.append(finding)
 
        return {"raw_text": text, "findings": results}
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
 