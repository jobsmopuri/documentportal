import sys
import uuid
from pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocuementPortalException
from datetime import datetime, timezone

class DocumentIngestion:
    """
    Handles saving, reading and combining of PDF's for comparision with session-based versioning.
    """
    def __init__(self,base_dir:str = "data\\document_compare",session_id = None):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.session_id = session_id or f"session_{datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")}_{uuid.uuid4().hex[:8]}"
        self.session_path = self.base_dir / self.session_id
        self.session_path.mkdir(parents=True, exist_ok=True)
        self.log.info("DocumentIngestion Initalized",session_path = str(self.session_path))
   

    def save_uploded_files(self,reference_file,actual_file):
        """
        Saves uploaded files to a specific directory
        """
        try:
            ref_path = self.session_path / reference_file.name
            actual_path = self.session_path / actual_file.name
            if not reference_file.name.lower().endswith(".pdf") or not actual_file.name.lower().endswith(".pdf"):
                raise ValueError("Only PDF files are allowed")
            
            with open(ref_path,"wb") as f:
                f.write(reference_file.getbuffer())

            with open(actual_path,"wb") as f:
                f.write(actual_file.getbuffer())

            self.log.info("files saved",reference = str(ref_path), actual = str(actual_path),sessiom=self.session_id)
            return ref_path, actual_path
        except Exception as ex:
            self.log.error(f"Error uploading file",ex)
            raise DocuementPortalException("An error occured while uploading file",sys)

    def read_pdf(self,pdf_path: Path) -> str:
        """
        reads a PDF file and extract the text from page.
        """
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError(f"PDF is encrypted : {pdf_path.name}") 
                all_text = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text() #type:ignore

                    if text.strip():
                        all_text.append(f"\n --- Page {page_num+1} ---\n {text}")
                self.log.info("PDF read Successfully", file=str(pdf_path),pages= len(all_text))
                return "\n".join(all_text)
        except Exception as ex:
            self.log.error(f"Error reading PDF",file=str(pdf_path), error=str(ex))
            raise DocuementPortalException("An error occured while reading the pdf",sys)
        
    def combine_documents(self) ->str:
        try:
            doc_parts = []
            self.log.info("Inside Combined_documents method")

            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file() and filename.suffix == ".pdf":
                    content = self.read_pdf(filename)
                    doc_parts.append(f"Document:{filename.name}\n{content}")
            

            combined_text = "\n\n".join(doc_parts)
            self.log.info("Documents Combined",count=len(doc_parts),session= self.session_id)
            return combined_text
        except Exception as ex:
            self.log.error(f"Error combine documents: {ex}",error = str(ex), session = self.session_id)
            raise DocuementPortalException("An error occured while combining documents.",sys)
        
    def clean_old_sessions(self, keep_latest:int = 3): 
        """
        Optional method to delete older session folders, keeping only the latest N
        """
        try:
            self.log.info("Inside Cleam Old Sessions ")
            session_folder = sorted(
                [f for f in self.base_dir.iterdir() if f.is_dir()],
                reverse=True
            )
            for folder in session_folder[keep_latest:]:
                for file in folder.iterdir():
                    file.unlink()
                folder.rmdir()
                self.log.info("Old session folder deleted", path=str(folder))
        except Exception as ex:
            self.log.error("Error cleaning old sessions",error=str(ex))
            raise DocuementPortalException("Error Cleaning old sessions",sys)
