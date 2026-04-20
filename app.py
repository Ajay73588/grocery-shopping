import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from minmax_report_agent import do_research, generate_report_content, save_to_docx

load_dotenv()

app = FastAPI()

os.makedirs("frontend", exist_ok=True)
os.makedirs("output", exist_ok=True)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

class GenerateRequest(BaseModel):
    topic: str
    filename: str
    model: str = "MiniMax-M2.7"

@app.post("/api/generate")
async def generate_report(req: GenerateRequest):
    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        return {"error": "MINIMAX_API_KEY environment variable not set."}

    filename = req.filename.strip()
    if not filename.endswith(".docx"):
        filename += ".docx"
    filename = os.path.basename(filename) # Prevent directory traversal
    
    output_path = os.path.join("output", filename)

    try:
        research_data, image_urls = do_research(req.topic)
        report_content = generate_report_content(req.topic, research_data, api_key, req.model, image_urls)
        save_to_docx(req.topic, report_content, output_path, image_urls)
        
        return {
            "success": True, 
            "markdown": report_content, 
            "download_url": f"/api/download/{filename}",
            "image_urls": image_urls
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/download/{filename}")
async def download_report(filename: str):
    filename = os.path.basename(filename)
    file_path = os.path.join("output", filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    return {"error": "File not found"}

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")
