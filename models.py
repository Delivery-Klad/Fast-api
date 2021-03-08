from pydantic import BaseModel


class Text(BaseModel):
    text: Optional[str] = None


class Assignees:
    Reporter: str
    Implementer: str


class Claims:
    Sub: str
    ITLabInterface: str
    ITLab: str
    Scope: str