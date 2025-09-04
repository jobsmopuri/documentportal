import uuid
import hashlib
import shutil
from pathlib import Path
from datetime import datetime , timezone
from typing import Optional,Iterable,List, Dict, Any
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocuementPortalException
log = CustomLogger().get_logger(__name__)
SUPPORTED_EXTENSIONS={".pdf",".docx",".txt"}

def _session_id(prefix:str="session")->str:
    return f"{prefix}_{datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")}_{uuid.uuid4().hex[:8]}"
def save_uploded_files(uploaded_files: Iterable, target_dir:Path)-> List[Path]:
    """
        Save uploded files (streamlit-like) and return local paths.
    """
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        saved: List[Path] = []
        for uf in uploaded_files:
            name = getattr(uf,"name","file")
            ext = Path(name).suffix.lower()
            if ext  not in SUPPORTED_EXTENSIONS:
                log.warning("Unsupported file skipped",filename= name)
                continue
            fname = f"{uuid.uuid4().hex[:8]}{ext}"
            out = target_dir / fname
            with open(out,"wb") as f:
                if hasattr(uf,"read"):
                    f.write(uf.read())
                else:
                    f.write(uf.getbuffer())
            saved.append(out)
            log.info("File saved for ingestion",uploaded = name,saved_as =str(out))
            return saved
    except Exception as ex:
        log.error("Failed to save uploded files",error=str(ex),dir=str(target_dir))
        raise DocuementPortalException("Failed to save uploded file",ex) from ex
