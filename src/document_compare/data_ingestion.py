import sys
from pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocuementPortalException

class DocumentComparator:
    def __init__(self):
        pass
    def delete_existing_file(self):
        """
        Deleting existing files at the specific path
        """
        pass
    def save_uploded_files(self):
        """
        Saves uploaded files to a specific directory
        """
        pass

    def read_pdf(self):
        """
        reads a PDF file and extract the text from page.
        """
        pass

