from pydantic import BaseModel, Field, RootModel
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


class ChangeFormat(BaseModel):
    Page: str
    Changes: str

class SummaryResponse(RootModel[list[ChangeFormat]]):
    pass