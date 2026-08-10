from typing import TypedDict


class State(TypedDict):
    question: str
    intent: str
    answer: str
    sources: list[str]
    confidence: float


