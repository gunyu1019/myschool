from typing import Any, Dict, Optional
from .intent import Intent
from .scene import Scene
from .session import Session
from .user import User
from .device import Device
from .context import Context


class Request:
    def __init__(self, payload: Dict[str, Any]):
        # Handler (Required)
        handler = payload.get("handler", {})
        self.handler = handler.get("name")

        # Intent (Required)
        intent = payload['intent']
        self.intent = Intent(intent)

        # Scene
        scene = payload.get("scene", {})
        self.scene = Scene.from_payload(scene) if scene is not None else None

        # Session (Required & Response Parameter)
        session = payload['session']
        self.session = Session.from_payload(session)

        # User (Required)
        user = payload['user']
        self.user = User(user)

        # Home
        home = payload.get('home')
        self.home: Optional[Dict[str, Any]] = home.get('params') if isinstance(home, Dict) else None

        # Device (Required)
        device = payload['device']
        self.device = Device.from_payload(device)

        # Context
        context = payload.get('context')
        self.context = Context(context) if context is not None else None
