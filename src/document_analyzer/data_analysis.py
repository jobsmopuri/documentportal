import os
import sys
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocuementPortalException
from models.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import  OutputFixingParser
from prompt.prompt_library import *

class DocumentAnalizer:
    """
    Analazes document using a pre-trained model
    Automatically logs all ations and supports session-based organization
    """
    def __init__(self):
        self.log = CustomLogger().get_logger(__name__)
        try:
            self.loader = ModelLoader()
            self.llm = self.loader.load_llm()
            #prepare Parsers
            self.parser = JsonOutputParser(pydentic_object = MetaData)
            self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser, llm=self.llm)
            #prompts
            self.prompt = prompt

            self.log.info("DocumentAlalizer instatiated successfully")

        except Exception as ex:
            self.log.error(f"Error Initaiated from DocumentAnalizer",ex)
            raise DocuementPortalException("Error in DocumentAnalizer initalization",sys)
    def analyze_metadata(self, document_path):
        try:
            model = self.model_loader.load_model()
            analysis_result = model.analyze(document_path)
            return self.fixing_parser.parser(analysis_result)
        except Exception as ex:
            raise DocuementPortalException("Error While in Analize document",ex) from ex



