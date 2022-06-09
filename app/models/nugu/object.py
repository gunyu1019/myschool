from typing import Any, Dict, Literal, Optional


class ImageObject:
    def __init__(
            self,
            url: str,
            size: Literal['X_SMALL', 'SMALL', 'MEDIUM', 'LARGE', 'X_LARGE'] = None,
            description: str = None,
            width=None,
            height=None
    ):
        self.description = description
        self._source = []

        base_source = {
            "url": url
        }
        if size is not None:
            base_source['size'] = size
        if width is not None:
            base_source['width'] = width
        if height is not None:
            base_source['height'] = height
        self._source.append(base_source)

    def to_dict(self):
        response = {
            "sources": self._source
        }
        if self.description is not None:
            response['contentDescription'] = self.description
        return response

    def add_resource(
            self,
            url: str,
            size: Literal['X_SMALL', 'SMALL', 'MEDIUM', 'LARGE', 'X_LARGE'] = None,
            width=None,
            height=None
    ):
        source = {
            "url": url
        }
        if size is not None:
            source['size'] = size
        if width is not None:
            source['width'] = width
        if height is not None:
            source['height'] = height
        self._source.append(source)

    def get_resource(
            self, position: int
    ):
        return self._source[position]['url']

    def remove_resource(
            self, position: int
    ):
        self._source.pop(position)


class TextObject:
    def __init__(
            self,
            text: str,
            color: str = None,
            display: Literal['none', 'block', 'inline'] = None,
            opacity: float = None,
            align: Literal['left', 'center', 'right'] = None,
            margin: int = None,
    ):
        self.text = text
        self.color = color
        self.style = {}
        if display is not None:
            self.style['display'] = display
        if opacity is not None:
            self.style['opacity'] = opacity
        if align is not None:
            self.style['align'] = align
        if margin is not None:
            self.style['margin'] = "{0}px".format(margin)

    def to_dict(self) -> Dict[str, Any]:
        response = {
            "text": self.text
        }
        if self.color is not None:
            response['color'] = self.color
        if self.style is not {}:
            response['style'] = self.style
        return response

    @property
    def display(self) -> Optional[Literal['none', 'block', 'inline']]:
        return self.style.get('display')

    @property
    def opacity(self) -> Optional[float]:
        return self.style.get('opacity')

    @property
    def align(self) -> Optional[Literal['left', 'center', 'right']]:
        return self.style.get('align')

    @property
    def margin(self) -> Optional[str]:
        return self.style.get('margin')


class ButtonObject:
    def __init__(self, text: str, token: str):
        self.text = text
        self.token = token

    def to_dict(self) -> Dict[str, str]:
        return {
            "text": self.text,
            "token": self.token
        }

