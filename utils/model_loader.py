import os
import sys
from dotenv import load_dotenv
from utils.config_loader import load_config
from logger.custom_logger import CustomLogger
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from exception.custom_exception import DocuementPortalException

log = CustomLogger.get_logger(__name__)

class ModelLoader:
    def __init__(self):
        """ initalize the configs and load the environment variables as well """
        load_dotenv()
        self._validate_env()
        self.config = load_config()
        log.info("Configurations loaded Successfully..",config_keys=list(self.config.keys()))

    def _validate_env(self):
        """ Validate the necessary environment variables.
        Ensure API keys exists 
        """
        required_vars=["GOOGLE_API_KEY","GROQ_API_KEY"]
        self.api_keys = {key:os.getenv(key) for key in required_vars}
        missing = [k for k,v in self.api_keys.items() if not v]
        if missing:
            log.error("Missing Environment Variables", missing_vars = missing)
            raise DocuementPortalException("Missing Environment variables",sys)
        log.info("ENvironment Variables Validated", available_keys=[k for k in self.api_keys if self.api_keys[k]])
    def load_embeddings(self):
        """ 
        Load and return the embeddings model.
        """
        try:
            log.info("Loading embedding model...")
            model_name = self.config["embedding_model"]["model_name"]
            return GoogleGenerativeAIEmbeddings(model = model_name)
        except Exception as e:
            log.error("Error loading embedding model",error = str(e))
            raise   DocuementPortalException("Failed to load  the embedding model",sys)      
    def load_llm(self):
        """
        Load the and return the model.
        Load LLM dynamically based on the provider in config..
        """
        llm_block = self.config["llm"]
        #default provider ENV
        provider_key = os.getenv("LLM_PROVIDER","groq")

        if provider_key not in llm_block:
            log.error("LLM provider not found in config",provider_key= provider_key)
            raise ValueError(f"Provider {provider_key} not found in config")
        
        llm_config = llm_block[provider_key]
        provider = llm_config.get("provider")
        model_name = llm_config.get("model_name")
        temparature = llm_config.get("temparature",0.2)
        max_token = llm_config.get("max_output_tokens",2048)

        log.info("Loading LLM ",provider = provider, model_name=model_name,temparature = temparature,max_token=max_token)

        if provider == "google":
            llm = ChatGoogleGenerativeAI(
                model = model_name,
                temparature = temparature,
                max_output_tokens = max_token
            )
            return llm
        elif provider == "groq":
            llm = ChatGroq(
                model = model_name,
                api_key = self.api_keys["GROQ_API_KEY"]
            )
            return llm
        else:
            log.error("Uunsupported LLM Provider",provider = provider)
            raise ValueError(f"Unsupported LLM Provider: {provider}")


# if __name__ == "__main__":
#     loader = ModelLoader()
#     embeddings = loader.load_embeddings()
#     print(f"Embedding model Loaded : {embeddings}")

#     llm = loader.load_llm()
#     print(f"LLM loaded : {llm}")

#     result = llm.invoke("Hello, How are you ?")
#     print(f"LLM Result : {result.content}")