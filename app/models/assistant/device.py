from enum import Enum
from typing import Any, Dict, List
from app.utils import get_enum


class Capability(Enum):
    UNSPECIFIED = "UNSPECIFIED"
    SPEECH = "SPEECH"
    RICH_RESPONSE = "RICH_RESPONSE"
    LONG_FORM_AUDIO = "LONG_FORM_AUDIO"
    INTERACTIVE_CANVAS = "INTERACTIVE_CANVAS"
    WEB_LINK = "WEB_LINK"
    HOME_STORAGE = "HOME_STORAGE"


class Timezone:
    def __init__(self, payload: Dict[str, Any]):
        self.id = payload['id']
        self.version = payload['version']


class Location:
    def __init__(self, payload: Dict[str, Any]):
        self.coordinates = payload.get('coordinates')
        self.postalAddress = payload.get('postalAddress')


class Device:
    def __init__(self, payload: Dict[str, Any]):
        capabilities = payload['capabilities']
        self.capabilities: List[Capability] = [
            get_enum(Capability, x) for x in capabilities
        ]

        location = payload.get('location')
        self.location = Location(location) if location is not None else None

        timezone = payload.get('timeZone')
        self.timezone = Timezone(timezone) if timezone is not None else None
