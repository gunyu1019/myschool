from typing import Dict, Union
from .base_interface import BaseInterface


class AudioPlayer(BaseInterface):
    def __init__(self, data: Dict[str, Union[int, str]]):
        super().__init__(data.get('token'))
        self.offset = int(data.get('offsetInMilliseconds', 0))
        self.activity = data['playerActivity']
