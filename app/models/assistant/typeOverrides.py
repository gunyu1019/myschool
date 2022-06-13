from enum import Enum
from typing import Optional, List, Dict, Any
from app.utils.enum import get_enum
from .synonym import SynonymType


class TypeOverrideMode(Enum):
    TYPE_UNSPECIFIED = "TYPE_UNSPECIFIED"
    TYPE_REPLACE = "TYPE_REPLACE"
    TYPE_MERGE = "TYPE_MERGE"


class TypeOverride:
    def __init__(
            self,
            name: str,
            mode: TypeOverrideMode,
            synonym: Optional[List[SynonymType]] = None
    ):
        self.name = name
        self.mode = mode
        self.synonym = synonym

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]):
        synonym = None
        if "synonym" in payload:
            synonym = SynonymType(payload["synonym"])

        return cls(
            name=payload['name'],
            mode=get_enum(TypeOverrideMode, payload['mode']),
            synonym=synonym
        )