import copy
from datetime import date as dt_module
from datetime import datetime
from typing import Optional

from flask import Blueprint
from flask import request as req
from werkzeug.datastructures import MultiDict

from app.config.config import get_config
from app.module import Client, NotFound, RequestsExcetion, School
from app.response import Response

bp = Blueprint(
    name="school_api",
    import_name="school_api",
    url_prefix="/api"
)

allergy_lists = ["난류", "우유", "메밀", "땅콩", "대두", "밀", "고등어", "게", "새우", "돼지고기", "복숭아",
                 "토마토", "아황산염", "호두", "닭고기", "쇠고기", "오징어", "조개류(굴,전복,홍합 등)"]


@bp.route("/school", methods=['GET'])
def school():
    return school_invoke(parameter=req.args).get_flask_response()


@bp.route("/meal", methods=['GET'])
def meal():
    return meal_invoke(req.args).get_flask_response()


def school_invoke(parameter: MultiDict):
    parser = get_config()
    if not parser.has_option("token", "neis"):
        return Response(
            {
                "CODE": 401,
                "MESSAGE": "neis OpenAPI token is missing."
            }, 401
        )

    if "name" not in parameter:
        return Response(
            {
                "CODE": 400,
                "MESSAGE": "Missing school name."
            },
            400
        )

    name: Optional[str] = parameter.get("name", default=None)
    provincial: Optional[str] = parameter.get("provincial", default=None)
    sc_code: Optional[str] = parameter.get("code", default=None)
    sc_type: Optional[int] = parameter.get("type", default=None, type=int)
    page: Optional[int] = parameter.get("page", default=1, type=int)

    if sc_type is not None and not 0 <= sc_type < 4:
        # 0: 초등학교 / 1: 중학교 / 2: 고등학교 / 3: 특수학교
        return Response(
            {
                "CODE": 400,
                "MESSAGE": "Type index out of range. ( 0 <= {0} <= 3)".format(
                    sc_type
                )
            }, 400
        )

    client = Client(
        token=parser.get('token', 'neis')
    )

    try:
        result = client.school(
            provincial_code=provincial,
            school_id=sc_code,
            kind=sc_type,
            name=name
        )
    except NotFound:
        return Response(
            {
                "CODE": 404,
                "MESSAGE": "Not Found"
            }, 404 )
    except RequestsExcetion as error:
        return Response(
            {
                "CODE": 500,
                "MESSAGE": "An unknown error occurred in API server.",
                "ERROR": error.__class__.__name__
            }, 500 )
    # Based on https://open.neis.go.kr/
    total = 0
    final_result = []
    for h in result.head:
        if "list_total_count" not in h:
            continue
        total = h["list_total_count"]

    for _sc in result.body:
        _sc: School
        final_result.append({
            "provincial_code": _sc.sc_code,
            "provincial": _sc.ofcdc,
            "code": _sc.sd_code,
            "name": _sc.name,
            "eng_name": _sc.eng_name,
            "type": _sc.type,
            "address": _sc.address1,
            "telephone": _sc.telephone,
            "website": _sc.website
        })

    return Response(
        {
            "data": final_result,
            "total": total,
            "current": page
        }, 200
    )


def meal_invoke(parameter: MultiDict):
    parser = get_config()
    if not parser.has_option("token", "neis"):
        return Response(
            {
                "CODE": 401,
                "MESSAGE": "neis OpenAPI token is missing."
            }, 401
        )
    if "provincial" not in parameter:
        return Response(
            {
                "CODE": 400,
                "MESSAGE": "Missing provincial."
            }, 400
        )
    if "code" not in parameter:
        return Response(
            {
                "CODE": 400,
                "MESSAGE": "Missing school code."
            }, 400
        )
    if "date" in parameter and ("startDate" in parameter or "endDate" in parameter):
        return Response(
            {
                "CODE": 400,
                "MESSAGE": "Don't put in start/end date and date at the same time."
            }, 400
        )
    if "startDate" in parameter and "endDate" not in parameter:
        return Response(
            {
                "CODE": 400,
                "MESSAGE": "Missing end date."
            }, 400
        )
    if "startDate" not in parameter and "endDate" in parameter:
        return Response(
            {
                "CODE": 400,
                "MESSAGE": "Missing start date."
            }, 400
        )

    provincial: str = parameter["provincial"]
    sd_code: str = parameter["code"]
    page: Optional[int] = parameter.get("page", default=1, type=int)

    _date: Optional[str] = parameter.get(
        "date",
        default=dt_module.today().strftime("%Y%m%d")
    )
    date: datetime = datetime.strptime(
        _date, "%Y%m%d"
    )
    start_date: Optional[str] = parameter.get("startDate", default=None)
    end_date: Optional[str] = parameter.get("endDate", default=None)

    client = Client(
        token=parser.get('token', 'neis')
    )

    try:
        result = client.meal(
            sd_code=sd_code,
            sc_code=provincial,
            date=date,
            from_date=start_date,
            to_date=end_date,
            page=page
        )
    except NotFound:
        return Response(
            {
                "CODE": 404,
                "MESSAGE": "Not Found"
            }, 404
        )
    except RequestsExcetion as error:
        return Response(
            {
                "CODE": 500,
                "MESSAGE": "An unknown error occurred in API server.",
                "ERROR": error.__class__.__name__
            }, 500
        )

    # Based on https://open.neis.go.kr/
    final_result = []

    for _sc in result.body:
        final_result.append({
            "provincial": _sc.ofcdc,
            "name": _sc.school,
            "date": _sc.date,
            "calorie": _sc.calorie,
            "type": _sc.type,
            "meal": _sc.meal,
            "allergy": _sc.allergy,
            "origin": _sc.origin,
            "nutrition": _sc.nutrition
        })

    if start_date is None and end_date is None and 0 < len(final_result) < 4:
        tp = 1
        _mt_md = {
            "조식": None,
            "중식": None,
            "석식": None
        }
        for _meal in final_result:
            _mt_md[_meal["type"]] = {
                "meal": _meal["meal"],
                "allergy": _meal["allergy"],
                "origin": _meal["meal"],
                "nutrition": _meal["nutrition"]
            }
        _final_result = copy.copy(final_result[0])

        _final_result.pop("meal")
        _final_result.pop("allergy")
        _final_result.pop("origin")
        _final_result.pop("nutrition")

        _final_result["breakfast"] = _mt_md["조식"]
        _final_result["lunch"] = _mt_md["중식"]
        _final_result["dinner"] = _mt_md["석식"]
    else:
        tp = 0
        _final_result = final_result

    return Response(
        {
            "type": tp,
            "data": _final_result,
            "current": page
        }, 200
    )
