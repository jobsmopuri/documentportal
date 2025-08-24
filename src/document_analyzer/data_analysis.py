import os
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocuementPortalException
from models.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import  OutputFixingParser

class DocumentAnalizer:
    """
    Analazes document using a pre-trained model
    Automatically logs all ations and supports session-based organization
    """
    def __init__(self):
        pass
    def analyze_metadata(self, document_path):
        try:
            model = self.model_loader.load_model()
            analysis_result = model.analyze(document_path)
            return self.fixing_parser.parser(analysis_result)
        except Exception as ex:
            raise DocuementPortalException("Error While in Analize document",ex) from ex



