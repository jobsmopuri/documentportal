import sys
from pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocuementPortalException

class DocumentIngestion:
    def __init__(self,base_dir:str = "data\\document_compare"):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    def delete_existing_file(self):
        """
        Deleting existing files at the specific path
        """
        try:
            if self.base_dir.exists() and self.base_dir.is_dir():
                for file in self.base_dir.iterdir():
                    if file.is_file():
                        file.unlink()
                        self.log.info("File deleted",path=str(file))
                self.log.info("Directory cleaned",directory = str(self.base_dir))
        except Exception as ex:
            self.log.error(f"Error while deleting file",ex)
            raise DocuementPortalException("An error occured while deleting the file",sys)

    def save_uploded_files(self,reference_file,actual_file):
        """
        Saves uploaded files to a specific directory
        """
        try:
            self.delete_existing_file()
            self.log.info("Existing file deleted successfully..")
            ref_path = self.base_dir//reference_file.name
            actual_path = self.base_dir//actual_file.name
            if reference_file.name.endswith(".pdf") or not actual_file.name.endswith(".pdf"):
                raise ValueError("Only PDF files are allowed")
            
            with open(ref_path,"wb") as f:
                f.write(reference_file.getbuffer())
            with open(actual_path,"wb") as f:
                f.write(actual_file.getbuffer())

            self.log.info("files saved",reference = str(ref_path), actual = str(actual_path))
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
                    text = page.get_text()

                    if text.strip():
                        all_text.append(f"\n --- Page {page_num+1} ---\n {text}")

                self.log("PDF read Successfully", file=str(pdf_path),pages= len(all_text))
                return "\n".join(all_text)
        except Exception as ex:
            self.log.error(f"Error reading PDF",ex)
            raise DocuementPortalException("An error occured while reading the pdf",sys)
        
    def combine_documents(self,) ->str:
        try:
            content_dict = []
            doc_parts = []

            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file() and filename.suffix == ".pdf":
                    content_dict[filename.name] = self.read_pdf(filename)
            for filename, content in content_dict.items():
                doc_parts.append(f"Document: {filename} \n {content}")

            combined_text = "\n\n".join(doc_parts)
            self.log.info("Documents Combined",count=len(doc_parts))
            return combined_text
        except Exception as ex:
            self.log.error(f"Error combine documents: {ex}")
            raise DocuementPortalException("An error occured while combining documents.",sys)
        

