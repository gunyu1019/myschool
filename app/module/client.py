"""
MIT License

Copyright (c) 2021 gunyu1019

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from datetime import datetime
from typing import Union, Optional

from .school import School, SchoolType
from .exception import NotFound
from .model import Response
from .request import Requests, check_requests


class Client:
    """토큰 값을 저장하고, 학교와 학원의 기본 정보를 불러오기 위하여 사용됩니다.
        Parameters
        ----------
        token : Optional[str]
            https://open.neis.go.kr/portal/guide/actKeyPage.do 에서 발급 받은 토큰값이 들어갑니다.

        Attributes
        ----------
        requests
            NEIS Open API를 주고받는 aiohttp 형식의 웹 클라이언트입니다.
        token : str
            token 값이 들어가게 되어 있습니다.
    """
    def __init__(self, token: str = None):
        self.requests = Requests(token)
        self.token = token

    def school(
            self,
            school_id: str = None,
            name: str = None,
            kind: int = None,
            location: str = None,
            provincial_code: str = None,
            page: int = None
    ):
        """학교 정보를 불러옵니다.
            Parameters
            ----------
            school_id : Optional[str]
                학교 고유 번호가 들어갑니다.
            name : Optional[str]
                학교 명이 들어갑니다.
            kind : Optional[int]
                학교의 종류가 들어갑니다. (참조: :class:`SchoolType`)
            location : Optional[str]
                학교의 소재지가 들어가게 됩니다. (ex. 서울특별시)
            provincial_code : Optional[str]
                교육청 코드가 들어갑니다. (참조: :class:`Location`)
            page : Optional[int]
                페이지 번호가 들어갑니다.

            Returns
            ----------
            Response
                검색된 학교 목록이 들어가게 됩니다.
        """
        params = {
            "pSize": 1000
        }

        type_m = None
        if kind is not None and 0 <= kind <= 3:
            tp = ["초등학교", "중학교", "고등학교", "특수학교"]
            type_m = tp[kind]
            params["SCHUL_KND_SC_NM"] = type_m

        if name is not None:
            params['SCHUL_NM'] = name
        if provincial_code is not None:
            params["ATPT_OFCDC_SC_CODE"] = provincial_code
        if school_id is not None:
            params["SD_SCHUL_CODE"] = school_id
        if page is not None:
            params["pIndex"] = page

        json1 = self.requests.get(
            "/hub/schoolInfo",
            params=params
        )

        check_requests(json1)

        head, row = json1['schoolInfo']

        if len(row["row"]) == 0:
            return NotFound

        return Response(
            head=head["head"], body=[School.from_data(x, self.token) for x in row["row"]]
        )

    def meal(
            self,
            sc_code: str,
            sd_code,
            date: datetime = datetime.now(),
            from_date: Optional[datetime] = None,
            to_date: Optional[datetime] = None,
            page: int = None
    ):
        school = School(
            sc_code=sc_code,
            sd_code=sd_code,
            token=self.token
        )
        return school.meal(
            date=date,
            from_date=from_date,
            to_date=to_date
        )

    def timetable(
            self,
            sc_code: str,
            sd_code,
            kind: SchoolType,
            grade: Union[int, str],
            class_nm: Union[int, str],
            date: datetime = datetime.now(),
            from_date: Optional[datetime] = None,
            to_date: Optional[datetime] = None,
            semester: Union[int, str] = None,
            year: Union[int, str] = None,
            page: int = None
    ):
        school = School(
            sc_code=sc_code,
            sd_code=sd_code,
            kind=kind,
            token=self.token
        )
        return school.timetable(
            date=date,
            from_date=from_date,
            to_date=to_date,
            grade=grade,
            class_nm=class_nm,
            semester=semester,
            year=year
        )
