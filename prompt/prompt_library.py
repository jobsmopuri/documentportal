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


document_analysis_prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful capable assistant trained to analyze and summarize documents.
    Return ONLY valis JSON matching the exact schema below.

    {format_instructions}
    Analyze the doument:
    {document_text}
"""
)
document_comparison_prompt = ChatPromptTemplate.from_template(
    """
    You will be provided with content from two PDFs . Your tasks are as follows:
    1. Compare the content in two PDF's
    2. Identify the differences and not down the page numbers.
    3. The output you provided by the page wise comparison content.
    4. If any page do not have any change, mention it as "NO CHANGE"

    input_document:
    {combined_docs}

    your response should follow this format:
    {format_instruction}
"""
)
PROMPT_REGISTRY = {
    "document_analysis":document_analysis_prompt,
    "document_comparison":document_comparison_prompt
}