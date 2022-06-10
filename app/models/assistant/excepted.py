from typing import Any, Dict, List
from app.utils import get_enum


class Excepted:
    def __init__(self, speech: List[str]):
        self.speech = speech

    def to_dict(self):
        return {
            "speech": self.speech
        }
