from typing import Any, Dict


class Response:
    def __init__(
            self,
            version: str,
            result: str = 'OK'
    ):
        self.version = version
        self.result = result
        self.output = {}
        self.directives = []

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
