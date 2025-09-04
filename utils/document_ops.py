from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader,TextLoader
from logger.custom_logger import CustomLogger
from typing import Optional,Iterable,List, Dict, Any
from pathlib import Path
from exception.custom_exception import DocuementPortalException


log = CustomLogger().get_logger(__name__)
SUPPORTED_EXTENSIONS={".pdf",".docx",".txt"}

def load_documents(paths: Iterable[Path]) -> List[Document]:
    """ Load docs usin appropriate loaders based on extension"""
    docs: List[Document] = []
    try:
        for p in paths:
            ext = p.suffix.lower()
            if ext == ".pdf":
                loader = PyPDFLoader(str(p))
            elif ext == ".docx":
                loader = Docx2txtLoader(str(p))
            elif ext == ".txt":
                loader == TextLoader(str(p))
            else:
                log.warning("Upsupported extesion skipped",paths=str(p))
            docs.extend(loader.load())
        log.info("Document Loaded",count=len(docs))
        return docs
    except Exception as ex:
        log.error("Failed to loading documents",error=str(ex))
        raise DocuementPortalException("Error Loading documents",ex) from ex

def concat_for_analysis(docs: List[Document])->str:
    parts=[]
    for d in docs:
        src = d.metadata.get("source") or d.metadata.get("file_path") or "unknown"
        parts.append(f"\n--Source:{src} --\n{d.page_content}")
    return "\n".join(parts)


def concat_for_comparison(ref_docs: List[Document],act_docs: List[Document])-> str:
    left = concat_for_analysis(ref_docs)
    right = concat_for_analysis(act_docs)
    return f"<<REFERENCE_DOCUMENTS>>\n {left} \n\n <<ACTUAL_DOCUMENTS>>\n{right}"
