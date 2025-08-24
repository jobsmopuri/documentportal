from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any,Union

class MetaData(BaseModel):
    Summary: List[str] = Field(default_factory = list,description = "Summary of the documennts")
    Title: str
    Author: str
    DateCreated: str
    LastModifiedDate: str
    publisher: str
    Language: str
    PageCount: Union[int,str]
    SentimentTone:str
