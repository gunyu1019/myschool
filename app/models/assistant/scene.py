from typing import Any, Dict
from app.utils import get_enum
from .slot import SlotStatus, Slot, SlotMode, SlotFillingStatus


class Scene:
    def __init__(self, payload: Dict[str, Any]):
        # Name
        self.name = payload["name"]

        # Slot
        # self.slot_status = get_enum(SlotStatus, payload['slotStatus'])

        # Next Scene
        next_scene = payload.get('next', {})
        self.next = next_scene.get('name')
