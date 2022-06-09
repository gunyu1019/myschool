from typing import Any, Dict
from .intent import Intent
from .scene import Scene
from .session import Session


class Request:
    def __init__(self, payload: Dict[str, Any]):
        # Handler (Required)
        handler = payload.get("handler", {})
        self.handler = handler.get("name")

        # Intent (Required)
        intent = payload['intent']
        self.intent = Intent(intent)

        # Scene
        scene = payload.get("intent", {})
        self.scene = Scene(scene)

        # Session (Required & Response Parameter)
        session = payload['session']
        self.session = Session.from_payload(payload)

        # User (Required)
        user = payload['user']

        # Home
        home = payload.get('home')

        # Device (Required)
        device = payload['device']

        # Context
        context = payload.get('context')
