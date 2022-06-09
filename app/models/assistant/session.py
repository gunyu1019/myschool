from typing import Any, Dict, List, Optional
from .typeOverrides import TypeOverride


class Session:
    def __init__(
            self,
            session_id: str,
            params: Dict[str, Any],
            type_overrides: Optional[List[TypeOverride]],
            language: str
    ):
        self.id: str = session_id
        self.params: Dict[str, Any] = params
        self.type_overrides = type_overrides
        self.language = language

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]):
        return cls(
            session_id=payload['id'],
            params=payload.get('params', {}),
            type_overrides=[
                TypeOverride.from_payload(x) for x in payload['typeOverrides']
            ],
            language=payload['languageCode']
        )
