from typing import Any, Dict


class IntentParameter:
    def __init__(self, original: str, resolved: Any):
        self.original = original
        self.resolved = resolved


class Intent:
    def __init__(self, payload: Dict[str, Any]):
        self.name = payload['name']
        self._params = payload.get('params')
        self.query = payload.get('query')

    def param(self, key: str):
        data = self._params[key]
        return IntentParameter(
            original=data['original'], resolved=data['resolved']
        )
