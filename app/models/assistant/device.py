from enum import Enum
from typing import Any, Dict, List, Optional
from app.utils.enum import get_enum


class Capability(Enum):
    UNSPECIFIED = "UNSPECIFIED"
    SPEECH = "SPEECH"
    RICH_RESPONSE = "RICH_RESPONSE"
    LONG_FORM_AUDIO = "LONG_FORM_AUDIO"
    INTERACTIVE_CANVAS = "INTERACTIVE_CANVAS"
    WEB_LINK = "WEB_LINK"
    HOME_STORAGE = "HOME_STORAGE"


class Timezone:
    def __init__(self, timezone_id: str, version: str):
        self.id = timezone_id
        self.version = version

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]):
        timezone_id = payload['id']
        version = payload['version']
        return cls(
            timezone_id=timezone_id, version=version
        )


class Location:
    def __init__(self, coordinates, postal_address):
        self.coordinates = coordinates
        self.postal_address = postal_address

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]):
        coordinates = payload.get('coordinates')
        postal_address = payload.get('postalAddress')
        return cls(
            coordinates=coordinates, postal_address=postal_address
        )


class Device:
    def __init__(
            self,
            capabilities: List[Capability],
            location: Optional[Location] = None,
            timezone: Optional[Timezone] = None
    ):
        self.capabilities = capabilities
        self.location = location
        self.timezone = timezone

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]):
        capabilities = payload['capabilities']
        _capabilities: List[Capability] = [
            get_enum(Capability, x) for x in capabilities
        ]

        location = payload.get('location')
        _location = Location.from_payload(location) if location is not None else None

        timezone = payload.get('timeZone')
        _timezone = Timezone.from_payload(timezone) if timezone is not None else None
        return cls(
            capabilities=_capabilities, location=_location, timezone=_timezone
        )
