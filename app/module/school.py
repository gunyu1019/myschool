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
from enum import Enum
from typing import Optional, Union

from .exception import NotFound
from .model import *
from .request import Requests, check_requests

t_id = {"초등학교": "els", "중학교": "mis", "고등학교": "his", "특수학교": "sps"}


class SchoolType(Enum):
    """학교 종류에 대한 정보 값이 저장되어 있습니다.
        Attributes
        ----------
        Elementary : int
            초등학교를 의미합니다.
        Middle : int
            중학교를 의미합니다.
        High : int
            고등학교를 의미합니다.
        Special : int
            특수학교를 의미합니다.
    """
    Elementary = 0
    Middle = 1
    High = 2
    Special = 3


class School:
    """학교의 값이 저장되고, 이 클래스를 통하여 급식, 시간표, 학사 일정 등을 불러올 수 있습니다.

        Parameters
        ----------
        token : Optional[str]
            https://open.neis.go.kr/portal/guide/actKeyPage.do 에서 발급 받은 토큰값이 들어갑니다.
        data : Optional[dict]
            :class:`Client`의 값이 이어저 들어가게 구성되어 있습니다. 만약에 직접 사용하신 다면 이 매게변수에 아무런 값도 넣어주지 마세요.
        sc_code : Optional[str]
            교육청 코드가 들어가게 됩니다. 직접 사용하신 다면 이 값은 필수로 필요합니다. (참조: :class:`Location`)
        sd_code : Optional[str]
            해당 학교 고유번호가 들어가게 됩니다. 직접 사용하신 다면 이 값은 필수로 필요합니다.
        kind : Optional[int]
            학교의 종류가 들어갑니다. :def:`timetable`를 사용하기 위해서는 값을 넣으셔야합니다. (참조: :class:`SchoolType`)

        Attributes
        ----------
        data : Optional[dict]
            :class:`Client`에서 불러온 값이 저장됩니다.
        requests
            NEIS Open API를 주고받는 aiohttp 형식의 웹 클라이언트입니다.
        sc_code : str
            교육청 코드가 들어가게 됩니다.
        sd_code : str
            학교 고유번호가 들어가게 됩니다.
        ofcdc : Optional[str]
            학교가 소속된 관리 시/도 교육청 명칭이 들어가게 됩니다. (ex. 서울특별시교육청)
        name : Optional[str]
            학교 명칭이 들어가게 됩니다.
        name_ENG : Optional[str]
            학교 영문 명칭이 들어가게 됩니다.
        type : Optional[str]
            학교의 종류가 들어갑니다.
        provincial : Optional[str]
            학교의 소재지가 들어갑니다. (ex. 서울특별시)
        location : Optional[str]
            학교가 소속된 교육청의 값이 들어갑니다. (ex. 서울특별시교육청)
        post_address : Optional[str]
            학교의 우편번호가 들어갑니다.
        address1 : Optional[str]
            학교의 주소가 들어갑니다.
        address2 : Optional[str]
            학교의 세부주소가 들어갑니다.
        telephone : Optional[str]
            학교의 전화번호가 들어갑니다.
        website : Optional[str]
            학교의 사이트 주소가 들어갑니다.
        fax : Optional[str]
            학교의 팩스 번호가 들어갑니다.
        opening : Optional[datetime]
            학교의 개교일이 들어갑니다.
        anniversary : Optional[datetime]
            학교의 개교기념일이 들어갑니다.
    """

    def __init__(self, sc_code: str, sd_code, token: str = None, kind: Union[SchoolType, int] = None):
        self.requests = Requests(token)

        self.sc_code = sc_code
        self.sd_code = sd_code
        self.type: Optional[str] = None
        if kind is not None:
            tp = ["초등학교", "중학교", "고등학교", "특수학교"]
            if isinstance(kind, SchoolType):
                self.type = tp[kind.value]
            else:
                self.type = tp[kind]

        self._data = dict()
        self.ofcdc: Optional[str] = None
        self.name: Optional[str] = None
        self.eng_name: Optional[str] = None
        self.provincial: Optional[str] = None
        self.location: Optional[str] = None
        self.post_address: Optional[str] = None
        self.address1: Optional[str] = None
        self.address2: Optional[str] = None
        self.telephone: Optional[str] = None
        self.website: Optional[str] = None
        self.fax: Optional[str] = None
        self._opening: Optional[str] = None
        self._anniversary: Optional[str] = None

    @classmethod
    def from_data(cls, data: dict, token: str = None):
        new_cls = cls(
            sc_code=data['ATPT_OFCDC_SC_CODE'],
            sd_code=data['SD_SCHUL_CODE'],
            token=token
        )
        new_cls._data = data

        new_cls.ofcdc = data.get('ATPT_OFCDC_SC_NM')
        new_cls.name = data.get('SCHUL_NM')
        new_cls.eng_name = data.get('ENG_SCHUL_NM')
        new_cls.type = data.get('SCHUL_KND_SC_NM')
        new_cls.provincial = data.get('LCTN_SC_NM')
        new_cls.location = data.get('JU_ORG_NM')
        new_cls.post_address = data.get('ORG_RDNZC')
        new_cls.address1 = data.get('ORG_RDNMA')
        new_cls.address2 = data.get('ORG_RDNDA')
        new_cls.phone = data.get('ORG_TELNO')
        new_cls.site = data.get('HMPG_ADRES')
        new_cls.fax = data.get('ORG_FAXNO')
        new_cls._opening = data.get('FOND_YMD')
        new_cls._anniversary = data.get('FOAS_MEMRD')
        return new_cls

    @property
    def opening(self) -> Optional[datetime]:
        if self._opening is None:
            return
        return datetime.strptime(self._opening, "%Y%m%d")

    @property
    def anniversary(self) -> Optional[datetime]:
        if self._anniversary is None:
            return
        return datetime.strptime(self._anniversary, "%Y%m%d")

    def meal(
            self,
            date: datetime = datetime.now(),
            from_date: datetime = None,
            to_date: datetime = None,
            page: int = None
    ):
        """급식 정보를 불러옵니다.
            Parameters
            ----------
            date : Optional[datetime]
                조회하시는 급식 날짜가 들어갑니다.
            from_date : Optional[datetime]
                조회하시는 급식 날짜가 들어갑니다. 만약에 특정 기간을 조회하고 싶으시면 본 매게변수를 이용해주세요.
            to_date : Optional[datetime]
                조회하시는 급식 날짜가 들어갑니다. 만약에 특정 기간을 조회하고 싶으시면 본 매게변수를 이용해주세요.
            page : Optional[int]
                조회할 페이지가 들어갑니다.

            Returns
            ----------
            list[:class:`Meal`]
                조회된 급식 목록이 들어가게 됩니다.
        """
        params = {
            'pSize': 1000,
            'ATPT_OFCDC_SC_CODE': self.sc_code,
            'SD_SCHUL_CODE': self.sd_code
        }
        if page is not None:
            params["pIndex"] = page
        if from_date is not None and to_date is not None:
            params['MLSV_FROM_YMD'] = from_date.strftime("%Y%m%d")
            params['MLSV_TO_YMD'] = to_date.strftime("%Y%m%d")
            json2 = self.requests.get(
                "/hub/mealServiceDietInfo",
                params=params
            )
        else:
            params['MLSV_YMD'] = date.strftime("%Y%m%d")
            json2 = self.requests.get(
                "/hub/mealServiceDietInfo",
                params=params
            )

        check_requests(json2)

        if len(json2.get('mealServiceDietInfo')[1].get('row')) == 0:
            raise NotFound

        result = json2['mealServiceDietInfo']
        head, row = result

        return Response(
            head=head['head'],
            body=[Meal(x) for x in row['row']]
        )

    def timetable(
            self,
            grade: Union[int, str],
            class_nm: Union[int, str],
            date: datetime = datetime.now(),
            from_date: datetime = None,
            to_date: datetime = None,
            semester: Union[int, str] = None,
            year: Union[int, str] = None,
            page: int = None
    ):
        """시간표 정보를 불러옵니다.
            Parameters
            ----------
            grade : Union[int, str]
                학년이 들어갑니다.
            class_nm : Union[int, str]
                반 정보가 들어갑니다.
            date : Optional[datetime]
                조회하시는 급식 날짜가 들어갑니다.
            from_date : Optional[datetime]
                조회하시는 급식 날짜가 들어갑니다. 만약에 특정 기간을 조회하고 싶으시면 본 매게변수를 이용해주세요.
            to_date : Optional[datetime]
                조회하시는 급식 날짜가 들어갑니다. 만약에 특정 기간을 조회하고 싶으시면 본 매게변수를 이용해주세요.
            semester : Optional[Union[int, str]]
                학기 정보가 들어갑니다.
            year : Optional[Union[int, str]]
                학년 정보가 정보가 들어갑니다.
            page : Optional[int]
                조회할 페이지가 들어갑니다.

            Returns
            ----------
            list[:class:`Timetable`]
                조회된 시간표 목록이 들어가게 됩니다.
        """
        if isinstance(grade, int):
            grade = str(grade)
        if isinstance(class_nm, int):
            class_nm = str(class_nm)

        if isinstance(year, int):
            year = str(year)
        if isinstance(semester, int):
            semester = str(semester)

        class_nm = class_nm

        type_nm = self.type
        if type_nm is None:
            raise TypeError("To get a timetable, you need to fill out the kind of school.")
        if type_nm not in t_id:
            raise TypeError("This school is not a searchable type.")

        params = {
            'pSize': 1000,
            'ATPT_OFCDC_SC_CODE': self.sc_code,
            'SD_SCHUL_CODE': self.sd_code,
            'GRADE': grade,
            'CLASS_NM': class_nm
        }
        if year is not None:
            params['AY'] = year
        if semester is not None:
            params['SEM'] = semester
        if page is not None:
            params["pIndex"] = page
        if from_date is not None and to_date is not None:
            params['TI_FROM_YMD'] = from_date.strftime("%Y%m%d")
            params['TI_TO_YMD'] = to_date.strftime("%Y%m%d")
            json2 = self.requests.get(
                f"/hub/{t_id[type_nm]}Timetable",
                params=params
            )
        else:
            params['ALL_TI_YMD'] = date.strftime("%Y%m%d")
            json2 = self.requests.get(
                f"/hub/{t_id[type_nm]}Timetable",
                params=params
            )

        check_requests(json2)

        result = json2.get(f'{t_id[type_nm]}Timetable')
        head, row = result

        return Response(
            head=head['head'],
            body=[Timetable(x) for x in row['row']]
        )
