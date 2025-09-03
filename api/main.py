from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Dict, Any, Optional, List
import os

app = FastAPI(title="Document Portal API", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static",StaticFiles(directory="../Static"),name="static")
template = Jinja2Templates(directory="../templates")

@app.get("/", response_class=HTMLResponse)
async def serve_ui(request: Request):
    return template.TemplateResponse("index.html",{"request":request})

@app.get("/health")
def health() -> Dict[str,str]:
    return {"status": "ok","service":"document-portal"}

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)) -> Any:
    try:
        pass
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {ex}")
    
@app.post("/compare")
async def compare_docs(reference: UploadFile = File(...), actual: UploadFile = File(...))-> Any:
    try:
        pass
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Comparision failed: {ex}")

@app.post("/chat/index")
async def chat_build_index()-> Any:
    try:
        pass
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {ex}")
    
@app.post("/chat/query")
async def chat_query()-> Any:
    try:
        pass
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Query failed: {ex}")
