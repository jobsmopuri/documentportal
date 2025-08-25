import sys
from pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocuementPortalException

class DocumentIngestion:
    def __init__(self,base_dir):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    def delete_existing_file(self):
        """
        Deleting existing files at the specific path
        """
        try:
            pass
        except Exception as ex:
            self.log.error(f"Error while deleting file",ex)
            raise DocuementPortalException("An error occured while deleting the file",sys)

    def save_uploded_files(self):
        """
        Saves uploaded files to a specific directory
        """
        try:
            pass
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

