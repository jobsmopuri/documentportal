import sys
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocuementPortalException
from datetime import datetime, timezone
from utils.model_loader import ModelLoader
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader,TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import uuid

class DocumentIngestor:
    SUPPORTED_FILE_EXTENSION = [".pdf",".txt",".docx",".md"]

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

    def ingest_files(self,uploaded_files):
        try:
            documents =[]
            for uploaded_file in uploaded_files:
                ext = Path(uploaded_file.name).suffix.lower()
                if ext not in self.SUPPORTED_FILE_EXTENSION:
                    self.log.warning("unsupported file extension",filename=uploaded_file)
                    continue
                unique_filename = f"{uuid.uuid4().hex[:8]}{ext}"
                temp_path = self.session_temp_dir / unique_filename

                with open(temp_path,"wb") as f:
                    f.write(uploaded_file.read())
                self.log.info("File saved for ingestion:", filename = uploaded_file, saved_as = str(temp_path),session_id = self.session_id)

                if ext == ".pdf":
                    loader = PyPDFLoader(str(temp_path))
                elif ext == ".docx":
                    loader = Docx2txtLoader(str(temp_path))
                elif ext == ".txt":
                    loader = TextLoader(str(temp_path),encoding="utf-8")
                else:
                    self.log.warning("Unsupported file type encountered",filename = uploaded_file.name)
                    continue

                docs = loader.load()
                documents.extend(docs)

            if not documents:
                raise DocuementPortalException("No Valid documents loaded",sys)
            
            self.log.info("All documents loaded", total_docs = len(documents),session_id = self.session_id)
            return self._create_retriver(documents)
        except Exception as ex:
            self.log.info("Failed to ingestfiles",error=str(ex))
            raise DocuementPortalException("Ingestion error in DocumentIngestor file",sys)

    def _create_retriver(self,documents):
        try:
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
            chunks = splitter.split_documents(documents)
            self.log.info("Documents split into chunks",total_chunks=len(chunks),session_id = self.session_id)
            embeddings = self.model_loader.load_embeddings()
            vectorstore = FAISS.from_documents(documents=documents, embedding=embeddings)
            vectorstore.save_local(str(self.session_faiss_dir))
            self.log.info("FAISS index saved to disk",path=str(self.session_faiss_dir),session_id = self.session_id)
            retriever = vectorstore.as_retriever(search_type="similarity",search_kwargs={"k":5})

            self.log.info("FAISS retriever created and ready to use",session_id = self.session_id)
            return retriever

        except Exception as ex:
            self.log.info("Failed to create retriever",error=str(ex))
            raise DocuementPortalException("Retrival error in DocumentIngestor",sys)

    