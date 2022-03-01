from typing import Dict, Any, Optional, Union, Literal
from enum import Enum
from json import loads


class BaseInterface:
    def __init__(self, token: Optional[str]):
        self.token = token


class DisplayType(Enum):
    FullText1 = "Display.FullText1"
    FullText2 = "Display.FullText2"
    ImageText1 = "Display.ImageText1"
    ImageText2 = "Display.ImageText2"
    ImageText3 = "Display.ImageText3"
    ImageText4 = "Display.ImageText4"
    TextList1 = "Display.TextList1"
    TextList2 = "Display.TextList2"
    TextList3 = "Display.TextList3"
    TextList4 = "Display.TextList4"
    ImageList1 = "Display.ImageList1"
    ImageList2 = "Display.ImageList2"
    ImageList3 = "Display.ImageList3"


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


class Display(BaseInterface):
    def __init__(self, data: Dict[str, Union[int, str]]):
        super().__init__(data.get('token'))
        self.service_id = data.get('playServiceId')
        self.version = data['version']

        self._title = {}
        self._background = {}
        self.duration: Optional[Literal['SHORT', 'MID', 'LONG', 'LONGEST']] = None
        self.response_type: Optional[DisplayType] = None
        self.badge: Optional[bool] = None
        self.items = []
        self.content = {}
        self.caption: Optional[Union[TextObject, str]] = None

    def get_response(
            self,
            display_type: DisplayType = None,
            service_id: str = None
    ) -> Dict[str, Any]:
        response = {
            "token": self.token,
            "version": self.version,
            "playServiceId": service_id or self.service_id,
            "type": display_type.value or self.response_type,
            "duration": self.duration
        }
        if self.content is not {} and len(self.items) > 0:
            raise TypeError()

        if self._title != {}:
            response['title'] = self._title
        if self._background != {}:
            response['background'] = self._background
        if len(self.items) > 0:
            response['listItems'] = self.items
            if self.badge is not None:
                response['badgeNumber'] = self.badge
            if self.caption is not None:
                response['caption'] = self._get_text(self.caption)
        if self.content is not {}:
            response['content'] = self.content
        return response

    @staticmethod
    def _get_text(data: [str, TextObject]):
        res = data
        if isinstance(data, str):
            res = TextObject(data)
        return res.to_dict()

    def set_title(
            self,
            text: Union[str, TextObject],
            subtext: Union[str, TextObject] = None,
            logo: ImageObject = None,
            sub_icon: ImageObject = None,
            button: Union[str, TextObject] = None,
    ):
        self._title = {
            'text': self._get_text(text)
        }
        if subtext is not None:
            self._title['subtext'] = self._get_text(text)
        if logo is not None:
            self._title['logo'] = logo
        if sub_icon is not None:
            self._title['subicon'] = sub_icon
        if button is not None:
            self._title['button'] = self._get_text(button)

    def set_background(
            self,
            image: ImageObject = None,
            color: str = None,
            opacity: float = None
    ):
        if image is not None:
            self._background['image'] = image.to_dict()
        if color is not None:
            self._title['color'] = color
        if opacity is not None:
            self._title['opacity'] = opacity


class AudioPlayer(BaseInterface):
    def __init__(self, data: Dict[str, Union[int, str]]):
        super().__init__(data.get('token'))
        self.offset = int(data.get('offsetInMilliseconds', 0))
        self.activity = data['playerActivity']


class Response:
    def __init__(
            self,
            version: str,
            result: str = 'OK'
    ):
        self.version = version
        self.result = result
        self.output = {}
        self.directives = {}

    def set_output(self, key, value):
        self.output[key] = value

    def remove_output(self, key):
        del self.output[key]

    def get_output(self, key):
        return self.output[key]

    def to_dict(self) -> Dict[str, Any]:
        response = {
            "version": self.version,
            "resultCode": self.result,
            "output": self.output
        }
        if self.directives != {}:
            response['directives'] = self.directives
        return response


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
        if not self.is_player:
            return
        return Display(self._player)

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
