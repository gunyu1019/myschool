from requests import request
import json

from .exception import *


class Requests:
    def __init__(self, token: str):
        self.token = token
        self.BASE = "https://open.neis.go.kr"

    def request(self, method: str, path: str, **kwargs):
        params = {
            "KEY": self.token,
            "Type": "json"
        }
        url = "{0}{1}".format(self.BASE, path)

        if "params" not in kwargs:
            kwargs['params'] = params
        else:
            kwargs['params'].update(params)

        response = request(
            method, url, **kwargs
        )

        if response.headers.get("Content-Type").startswith("application/json;"):
            result = response.json()
        else:
            result = response.text
            result = json.loads(result)

        return result

    def get(self, path: str, **kwargs):
        return self.request(
            method="GET",
            path=path,
            **kwargs
        )


def check_requests(resp):
    """결과에 오류값이 있는 지 확인합니다.
        Parameters
        ----------
        resp : dict
            반환된 json 값이 포함됩니다.

        Raises
        ----------
        .exception.Notfound
            해당하는 데이터가 없습니다.
        .exception.Forbidden
            관리자에 의해 인증키 사용이 제한되거나, 인증키가 유효하지 않습니다.
        .exception.NotImplemented
            필수 값이 누락되어 있습니다. 요청인자를 참고 하십시오.
        .exception.TooManyRequests
            데이터요청은 한번에 최대 1,000건을 넘거나, 일별 트래픽 제한을 넘은 호출입니다. 일별 트래픽 제한을 초과하면 오늘은 더이상 호출할 수 없습니다.
        .exception.TooManyRequests
            서버 오류입니다. 지속적으로 발생시 OpenAPI 홈페이지로 문의(Q&A) 바랍니다.
    """
    if 'RESULT' in resp.keys():
        if 'CODE' in resp['RESULT'].keys():
            ercode = resp['RESULT']['CODE']
            if ercode == 'INFO-200':
                raise NotFound(resp['RESULT'])
            elif ercode == 'INFO-300' or ercode == 'ERROR-290':
                raise Forbidden(resp['RESULT'])
            elif ercode == 'ERROR-300' or ercode == 'ERROR-333':
                raise NotImplemented(resp['RESULT'])
            elif ercode == 'ERROR-336' or ercode == 'ERROR-337':
                raise TooManyRequests(resp['RESULT'])
            elif ercode == 'ERROR-500' or ercode == 'ERROR-600' or ercode == 'ERROR-601':
                raise InternalServerError(resp['RESULT'])
    return
