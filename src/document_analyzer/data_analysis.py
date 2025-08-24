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
        
    def analyze_document(self,document_text:str) -> dict:
        """
            Analize a document's text and extract structured metadata & summary
        """
        try:
            chain = self.prompt | self.llm | self.fixing_parser
            self.log.info("MetaData chain is intialized ")

            response = chain.invoke({
                "format_instructions": self.parser.get_format_instructions(),
                "document_text": document_text
            })
            self.log.info("Metadata Extraction successful",keys=list(response.keys()))
            return response
        except Exception as ex:
            self.log.error("Metadata Analysis Failed",error=str(ex))
            raise DocuementPortalException("Metadata Extraction Failed") from ex
        
        
    def analyze_metadata(self, document_path):
        try:
            model = self.model_loader.load_model()
            analysis_result = model.analyze(document_path)
            return self.fixing_parser.parser(analysis_result)
        except Exception as ex:
            raise DocuementPortalException("Error While in Analize document",ex) from ex



