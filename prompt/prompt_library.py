#prepare prompt template 
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful capable assistant trained to analyze and summarize documents.
    Return ONLY valis JSON matching the exact schema below.

    {format_instructions}
    Analyze the doument:
    {document_text}
"""
)