from pydantic import BaseModel
from typing import Optional


class Text(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None


class Assignees:
    Reporter: str
    Implementer: str
