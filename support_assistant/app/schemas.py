from pydantic import BaseModel


class RequestSchema(BaseModel):
    question: str


class ResponseSchema(BaseModel):
    answer: str
    sources: list[str]
    confidence: float