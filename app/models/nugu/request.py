from typing import Any, Dict, Optional
from json import loads
from .audio import AudioPlayer
from .display import Display
from .response import Response


class Request:
    def __init__(self, payload: Dict[str, Any]):
        self.version = payload['version']

        # Action
        action = payload['action']
        self.name = action['actionName']
        self.parameters = {}
        for x in action['parameters'].keys():
            self.parameters[x] = Parameter(
                action['parameters'][x]
            )

        # Event
        event = payload.get("event", {})
        self.event = event.get("type")

        # Context
        context = payload['context']
        session = context['session']
        self.id = session["id"]
        self.oauth = session.get("accessToken")
        self.is_new = bool(session["isNew"])
        self.is_test = session.get("isPlayBuilderRequest", False)

        device = context['device']
        self.device_type = device['type']
        self.state = device.get("state", {})

        interfaces = context['supportedInterfaces']
        self._display = interfaces.get("Display")
        self._player = interfaces.get("AudioPlayer")

    @classmethod
    def from_data(cls, data):
        return cls(
            loads(data.decode('utf8'))
        )

    @property
    def is_player(self) -> bool:
        return self._player is not None

    @property
    def is_display(self) -> bool:
        return self._display is not None

    @property
    def player(self) -> Optional[AudioPlayer]:
        if not self.is_player:
            return
        return AudioPlayer(self._player)

    @property
    def display(self) -> Optional[Display]:
        if not self._display:
            return
        return Display(self._display)

    def get_response(self, result: str = 'OK') -> Response:
        return Response(
            version=self.version,
            result=result
        )


class Parameter:
    def __init__(self, data: Dict[str, Optional[str]]):
        self.type: Optional[str] = data.get("type")
        self.value: str = data["value"]

    @classmethod
    def empty(cls):
        cls.value: Optional[str]
        return cls(
            data={"value": None}
        )

    def __str__(self) -> str:
        return self.value
