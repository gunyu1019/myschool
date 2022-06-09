from typing import Any, Dict, Optional, Union, Literal
from .base_interface import BaseInterface
from .display_type import DisplayType
from .object import TextObject, ImageObject


class Display(BaseInterface):
    def __init__(self, data: Dict[str, Union[int, str]]):
        super().__init__(data.get('token'))
        self.service_id = data.get('playServiceId')
        self.version = data['version']

        self._title = {}
        self._background = {}
        self.duration: Optional[Literal['SHORT', 'MID', 'LONG', 'LONGEST']] = None
        self.badge: Optional[bool] = None
        self.items = []
        self.content = {}
        self.caption: Optional[Union[TextObject, str]] = None

    def get_response(
            self,
            display_type: DisplayType,
            service_id: str = None
    ) -> Dict[str, Any]:
        response = {
            "token": self.token,
            "version": self.version,
            "playServiceId": service_id or self.service_id,
            "type": display_type.value,
            "duration": self.duration
        }
        if len(self.content) > 0 and len(self.items) > 0:
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
            icon: ImageObject = None,
            sub_icon: ImageObject = None,
            button: Union[str, TextObject] = None,
    ):
        self._title = {
            'text': self._get_text(text)
        }
        if subtext is not None:
            self._title['subtext'] = self._get_text(text)
        if icon is not None:
            self._title['logo'] = icon.to_dict()
        if sub_icon is not None:
            self._title['subicon'] = sub_icon.to_dict()
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
