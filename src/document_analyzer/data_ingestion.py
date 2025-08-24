import os
import fitz
import uuid
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocuementPortalException

class DocumentHandler:
    """
    Handles PDF saving and retrival operations:
    Automatically logs all actions and supports session-based organization 
    """
    def __init__(self, data_dir: str=None, session_id: str=None):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.data_dir = data_dir or os.getenv(
                "DATA_STORAGE_PATH",
                os.path.join(os.getcwd(),"data","doument_analysis")
            )
            self.session_id = session_id or f"session_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}_{uuid.uuid4().hex[:8]}"

            self.session_path = os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)

            self.log.info("PDF Handler Initated",session_id=self.session_id,session_path = self.session_path)
        except Exception as ex:
            self.log.info(f"Error while initalizing the DocumentHandler: {ex}")
            raise DocuementPortalException("Error while initalizing the DocumentHandler",ex) from ex

    def save_pdf(self,uploaded_file):
        try:
            filename = os.path.basename(uploaded_file.name)

            if not filename.lower().endswith(".pdf"):
                raise DocuementPortalException("Invalid file type . Only PDF files are allowed")
            
            save_path = os.path.join(self.session_path,filename)

            with open(save_path, "wb")as f:
                f.write(uploaded_file.getbuffer())
            self.log.info("PDF saved successfully",file=filename, save_path = save_path, session_id = self.session_id)
            return save_path
        
        except Exception as ex:
            self.log.info(f"Error while save the pdf: {ex}")
            raise DocuementPortalException("Error while save the pdf",ex) from ex
       
    def read_pdf(self, pdf_path:str) -> str:
        try:
            text_chunks =[]
            with fitz.open(pdf_path) as doc:
                for page_num, page in enumerate(doc,start=1):
                    text_chunks.append(f"\n---- Page {page_num} ----\n {page.get_text()}")
                text = "\n".join(text_chunks)
            
            self.log.info("PDF read successfully",pdf_path = pdf_path, session_id = self.session_id,pages = len(text_chunks))
            return text
        
        except Exception as ex:
            self.log.info(f"Error while reading the pdf: {ex}")
            raise DocuementPortalException("Error while reading the pdf",ex) from ex
    
if __name__ == "__main__":
    from pathlib import Path
    from io import BytesIO

    pdf_path = r"C:\\Users\\Sivakumar.Mopuri\\source\\repos\\LLMOPS\\document_portal\\data\\doument_analysis\\NIPS-2017-attention-is-all-you-need-Paper.pdf"

    class DummyFile:
        def __init__(self,file_path):
            self.name = Path(file_path).name
            self.file_path = file_path
        def getbuffer(self):
            return open(self.file_path,"rb").read()
        
    dummy_pdf = DummyFile(pdf_path)
    handler = DocumentHandler()

        
    try:
        saved_path = handler.save_pdf(dummy_pdf)
        print(saved_path)

        content = handler.read_pdf(saved_path)
        print("PDF Content")
        print(content[:500])
    except Exception as ex:
        print(f"Error: {ex}")