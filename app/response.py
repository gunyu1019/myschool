from flask import make_response
from flask import Response as Res
from flask import jsonify
from typing import Union


class Response:
    def __init__(self, data, status=200, **kwargs):
        self.data = data
        self.status = status
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])
        self.__kwargs_key = kwargs.keys()
        self.__kwargs = kwargs

    def get_flask_response(self) -> Res:
        return make_response(
            self.convert_data(),
            self.status,
            *[self.__kwargs[key] for key in self.__kwargs_key]
        )

    def convert_data(self) -> Union[Res, str]:
        if isinstance(self.data, dict) or isinstance(self.data, list):
            return jsonify(self.data)
        return self.data
