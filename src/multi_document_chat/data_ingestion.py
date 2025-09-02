import sys
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocuementPortalException
from datetime import datetime, timezone
from utils.model_loader import ModelLoader
import uuid

class DocumentIngestor:
    SUPPORTED_FILE_EXTENSION = {".pdf",".txt",".docx",".md"}

    def __init__(self,temp_dir:str="data/multi_doc_chat",faiss_dir:str="faiss_index",session_id:str | None=None):
        try:
            self.log = CustomLogger.get_logger(__name__)
            self.temp_dir = temp_dir
            self.faiss_dir = faiss_dir
            self.temp_dir.mkdir(parents=True,exits_ok = True )
            self.faiss_dir.mkdir(parents=True,exits_ok = True )

            self.session_id = session_id or f"session_{datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")}_{uuid.uuid4().hex[:8]}"
            self.session_temp_dir = self.temp_dir / self.session_id
            self.session_faiss_dir = self.faiss_dir / self.session_id
            self.session_temp_dir.mkdir(parents=True,exits_ok = True )
            self.session_faiss_dir.mkdir(parents=True,exits_ok = True )

            self.model_loader = ModelLoader()
            self.log.inof(
                "DocumentIngestor intstatialized..",
                temp_base = str(temp_dir),
                faiss_base = str(faiss_dir),
                session_id = self.session_id,
                temp_path = str(self.session_temp_dir),
                faiss_path = str(self.session_faiss_dir)
            )
            

        except Exception as ex:
            self.log.info("Failed to initalize DocumentIngestor",error=str(ex))
            raise DocuementPortalException("Initilization error in DocumentImgestor",sys)

    def ingest_files(self):
        try:
            pass
        except Exception as ex:
            self.log.info("Failed to ingestfiles",error=str(ex))
            raise DocuementPortalException("Ingestion error in DocumentIngestor file",sys)

    def _create_retriver(self,documents):
        try:
            pass
        except Exception as ex:
            self.log.info("Failed to create retriever",error=str(ex))
            raise DocuementPortalException("Retrival error in DocumentIngestor",sys)

    