from enum import Enum
from typing import Any, Dict
from app.utils import get_enum


class SlotFillingStatus(Enum):
    UNSPECIFIED = "UNSPECIFIED"
    INITIALIZED = "INITIALIZED"
    COLLECTING = "COLLECTING"
    FINAL = "FINAL"


class Slot:
    def __init__(self, payload: Dict[str, Any]):
        self.mode = get_enum(SlotStatus, payload.get('mode')) if 'mode' in payload else None
        self.status = get_enum(SlotStatus, payload['status'])
        self.value = payload.get('value')
        self.updated = payload.get('updated')
        self.prompt = payload.get('prompt')


class SlotMode(Enum):
    MODE_UNSPECIFIED = "MODE_UNSPECIFIED"
    OPTIONAL = "OPTIONAL"
    REQUIRED = "REQUIRED"


class SlotStatus(Enum):
    SLOT_UNSPECIFIED = "SLOT_UNSPECIFIED"
    EMPTY = "EMPTY"
    INVALID = "INVALID"
    FILLED = "FILLED"