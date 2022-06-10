from typing import Any, Dict, List
from app.utils import get_enum


class MediaContext:
    def __init__(self, payload: Dict[str, Any]):
        self.progress = payload.get('progress')
        self.index: int = int(payload.get('index', 0))


class CanvasContext:
    def __init__(self, payload: Dict[str, Any]):
        self.state = payload.get('state')


class Context:
    def __init__(self, payload: Dict[str, Any]):
        media = payload.get('media')
        self.media = MediaContext(media) if media is not None else None

        canvas = payload.get('canvas')
        self.canvas = CanvasContext(canvas) if canvas is not None else None
