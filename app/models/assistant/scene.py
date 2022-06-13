from typing import Any, Dict, Optional
from app.utils.enum import get_enum
from .slot import Slot, SlotFillingStatus


class Scene:
    def __init__(
            self,
            name: str,
            slot_status: SlotFillingStatus,
            slots: Optional[Dict[str, Slot]] = None,
            next: Optional[str] = None
    ):
        self.slot_status = slot_status
        self.name = name
        self.slot = slots
        self.next = next

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]):
        # Name
        name = payload["name"]

        # Slot
        slot_status = get_enum(SlotFillingStatus, payload['slotFillingStatus'])
        slot = {
            key: Slot(value) for key, value in payload.get('slots', {}).items()
        }

        # Next Scene
        next_scene = payload.get('next', {})
        next = next_scene.get('name')

        return cls(
            name=name, slots=slot, slot_status=slot_status, next=next
        )
