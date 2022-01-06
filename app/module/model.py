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
from  datetime import datetime
from typing import Optional

allergy_lists = ["난류", "우유", "메밀", "땅콩", "대두", "밀", "고등어", "게", "새우", "돼지고기", "복숭아", "토마토", "아황산염", "호두",
                 "닭고기", "쇠고기", "오징어", "조개류(굴,전복,홍합 등)"]


class Response:
    def __init__(self, **kwargs):
        self.head = None
        self.body = None
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])


class Meal:
    """급식 정보를 포함합니다. 급식 정보에 대한 알레르기, 영양분 정보가 포함되어 있습니다.
        Attributes
        ----------
        data : dict
            이 모델의 원본 형태의 내용이 포함되어 있습니다.
        school : str
            학교 이름이 리턴됩니다.
        code : str
            식사코드가 리턴됩니다.
        type : str
            급식의 종류가 리턴됩니다. 대표적으로 조식(), 중식(점심), 석식(저녁)으로 구성되어 있습니다.
        calorie : str
            급식의 칼로리 정보가 리턴됩니다.
        meal : list
            급식 정보가 포함되어 있습니다.
    """
    def __init__(self, response):
        self.data = response

        self.ofcdc = response.get('ATPT_OFCDC_SC_NM')
        self.school = response.get("SCHUL_NM")
        self.code = response.get("MMEAL_SC_CODE")
        self.type = response.get("MMEAL_SC_NM")
        self._date = response.get("MLSV_YMD")
        self.calorie = response.get("CAL_INFO")

        self.meal = response.get("DDISH_NM").split("<br/>")
        self._origin = response.get("ORPLC_INFO").split("<br/>")
        self._nutrition = response.get("NTR_INFO").split("<br/>")

    @property
    def date(self) -> Optional[datetime]:
        if self._date is None:
            return
        return datetime.strptime(self._date, "%Y%m%d")

    @property
    def allergy(self):
        allergy = []
        for i in enumerate(self.meal):
            allergy_cache = []
            for j in range(18, 0, -1):
                if "{}.".format(j) in self.meal[i[0]]:
                    allergy_cache.append(allergy_lists[j - 1])
                self.meal[i[0]] = self.meal[i[0]].replace("{}.".format(j), "")
            allergy.append(allergy_cache)
        return allergy

    @property
    def origin(self):
        origin = dict()
        for i in self._origin:
            key = i.split(":")[0].strip()
            value = i.split(":")[1].strip()
            origin[key] = value
        return origin

    @property
    def nutrition(self):
        nutrition = dict()
        for i in self._nutrition:
            key = i.split(":")[0].strip()
            value = i.split(":")[1].strip()
            nutrition[key] = value
        return nutrition


class Timetable:
    """시간표 정보가 포함됩니다. 시간표 정보는 n교시 마다 배열로 정보가 따로 있습니다. 따라서 그 날짜에 시간표를 불러온다면 시간표 정렬이 필요합니다.
        Attributes
        ----------
        data : dict
            이 모델의 원본 형태의 내용이 포함되어 있습니다.
        school : str
            학교 이름이 리턴됩니다.
        title : str
            과목명이 리턴됩니다.
        time : list
            과목에 따른 n 시간이 리턴됩니다.
        semester : str
            학기 정보가 리턴됩니다.
        year : str
            학년도 정보가 리턴됩니다.
        grade : str
            학년 정보가 리턴됩니다.
        class_nm : list
            반 정보가 리턴됩니다.
    """
    def __init__(self, response):
        self.data = response

        self.school = response.get("SCHUL_NM")
        self.title = response.get("ITRT_CNTNT")
        self.semester = response.get("SEM")
        self.year = response.get("AY")
        self._date = response.get("ALL_TI_YMD")
        self.grade = response.get("GRADE")
        self.class_nm = response.get("CLASS_NM")
        self.time = response.get("PERIO")

    @property
    def date(self) -> Optional[datetime]:
        if self._date is None:
            return
        return datetime.strptime(self._date, "%Y%m%d")
