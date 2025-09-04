from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Dict, Any, Optional, List
from src.document_ingestion.document_ingestion import (
    DocHandler,
    DocumentCompartor,
    ChatIngestor,
    FaissManager
)
from src.document_analyzer.data_analysis import DocumentAnalizer
from src.document_compare.document_comparer import DocumentComparatorLLM
from src.document_chat.retriever import ConversationalRAG
import os

app = FastAPI(title="Document Portal API", version="0.1")
FAISS_BASE = os.getenv("FAISS_BASE","faiss_index")
UPLOAD_BASE = os.getenv("UPLOAD_BASE","data")

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

class FastAPIFileAdapter:
    """ Adapt FastApi UplodedFile -> .name + .getbuffer() API"""
    def __init__(self,uf: UploadFile):
        self._uf = uf
        self.name = uf.filename
    def getbuffer(self) -> bytes:
        self._uf.file.seek(0)
        return self._uf.file.read()

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)) -> Any:
    try:
        docHandler = DocHandler()
        saved_path = docHandler.save_pdf(FastAPIFileAdapter(file))
        text = _read_pdf_via_handler(docHandler,saved_path)
        analizer = DocumentAnalizer()
        result = analizer.analyze_metadata(text)
        return JSONResponse(content = result)
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {ex}")
    
@app.post("/compare")
async def compare_docs(reference: UploadFile = File(...), actual: UploadFile = File(...))-> Any:
    try:
        docCompare = DocumentCompartor()
        ref_path , act_path = docCompare.save_uploded_files(FastAPIFileAdapter(reference),FastAPIFileAdapter(actual))
        _ = ref_path,act_path
        combined_text = docCompare.combine_documents()
        comp = DocumentComparatorLLM()
        df = comp.compare_documents(combined_text)
        return {"rows": df.to_dict(orient="records"),"session_id":docCompare.session_id}
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Comparision failed: {ex}")

@app.post("/chat/index")
async def chat_build_index(
    files: List[UploadFile: File(...)],
    session_id: Optional[str] = Form(None),
    use_session_dirs: bool = Form(None),
    chunk_size: int = Form(1000),
    chunk_overlap: int = Form(200),
    k: int = Form(5)
)-> Any:
    try:
        wrapped = [FastAPIFileAdapter(f) for f in files]
        chatIngestor = ChatIngestor(
            temp_base = UPLOAD_BASE,
            faiss_base = FAISS_BASE,
            use_session_dirs = use_session_dirs,
            session_id = session_id or None
        )
        chatIngestor.build_retriver(wrapped, chunk_size=chunk_size, chunk_overlap = chunk_overlap, k=k)
        return {"session_id": chatIngestor.session_id,"k":k, "use_session_dir": use_session_dirs}
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {ex}")
    
@app.post("/chat/query")
async def chat_query(
    question: str = Form(...),
    session_id: Optional[str]= Form(None),
    use_session_dirs: bool = Form(True),
    k:int =Form(5)
)-> Any:
    try:
        if use_session_dirs and not session_id:
            raise HTTPException(status_code=400, detail="session_id is required when use_session_dir is True")
        # Prepare faiss index path 
        index_dir = os.path.join(FAISS_BASE, session_id) if use_session_dirs else FAISS_BASE
        if not os.path.isdir(index_dir):
            raise HTTPException(status_code=404, detail=f"FAISS index was not found at: {index_dir}")
        rag = ConversationalRAG(session_id=session_id)
        rag.load_retriever_from_faiss(index_dir)
        response = rag.invoke(question, chat_history=[])

        return {
            "answer": response,
            "session_id": session_id,
            "k":k,
            "engine": "LCEL-RAG"
        }
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Query failed: {ex}")



def _read_pdf_via_handler(handler: DocHandler, path:str) -> str:
    """
        Helper function to read PDF using DocHandler
    """
    try:
        if hasattr(handler,"read_pdf"):
            return handler.read_pdf(path)
        if hasattr(handler,"read_"):
            return handler.read_pdf(path)
        return RuntimeError("DocHandler Has neither read_pdf nor read_ method.")
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error reading PDF: {str(ex)}")
    