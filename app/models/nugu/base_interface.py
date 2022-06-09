from typing import Optional


class BaseInterface:
    def __init__(self, token: Optional[str]):
        self.token = token
