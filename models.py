from pydantic import BaseModel
from typing import Optional


class Text(BaseModel):
    text: Optional[str] = None


class Assignees:
    Reporter: str
    Implementer: str
