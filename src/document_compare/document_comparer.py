import sys
from dotenv import load_dotenv
import pandas as pd
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocuementPortalException
from models.models import *
from prompt.prompt_library import PROMPT_REGISTRY
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

class DocumentComparatorLLM:
    def __init__(self):
        load_dotenv()
        self.log = CustomLogger().get_logger(__name__)
        self.loader = ModelLoader()
        self.llm = self.loader.load_llm()
        self.parser = JsonOutputParser(pydantic_object=SummaryResponse)
        self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser, llm = self.llm)
        self.prompt = PROMPT_REGISTRY["document_comparison"]
        self.chain = self.prompt | self.llm | self.parser
        self.log.info("DocumentComparatorLLM initalized with model and parser")
    def compare_documents(self):
        """
        Compares two documents and returns a structured comparision
        """
        try:
            pass
        except Exception as ex:
            self.log.error(f"Error occured in compare_document: {ex}")
            raise DocuementPortalException("An error occured while comparing the documents",sys)
    def _format_response(self):
        """ 
        Formats the response from the LLM into a strctured format
        """
        try:
            pass
        except Exception as ex:
            self.log.error("Error formatting response into DataFrame", error = str(ex))
            raise DocuementPortalException("Error formatting Response",sys)


