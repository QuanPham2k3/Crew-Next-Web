from typing import List
from pydantic import BaseModel


class NamedUrl(BaseModel):
    name: str
    url: str

class SearchInfo(BaseModel):
    topic: str
    category: str
    web_urls: List[str]
    

class SearchInfoList(BaseModel):
    searchs: List[SearchInfo]
