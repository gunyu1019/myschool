from typing import List

from flask import Blueprint
from flask import abort
from flask import jsonify
from flask import request
from flask import send_file
from werkzeug.datastructures import MultiDict

from app.config.config import get_config
from app.directory import directory
from app.models.nugu import *
from app.module.school import School
from app.response import Response
from app.utils.date import DateConvert
from .api import school_invoke, meal_invoke, timetable_invoke

bp = Blueprint(
    name="nugu_backend",
    import_name="nugu_backend",
    url_prefix="/school/nugu"
)


@bp.route("/health", methods=['GET'])
def health():
    return 'OK'


@bp.route("/icon", methods=['GET'])
def icon_nugu():
    return send_file(
        '{0}/static/logo-for-nugu.png'.format(directory),
        mimetype='image/png'
    )


@bp.route("/meal", methods=['POST'])
def meal_nugu():
    try:
        req = Request.from_data(request.data)
    except KeyError:
        raise abort(403)
    # print([(x, req.parameters[x].value) for x in req.parameters])

    parser = get_config()
    if req.parameters.get('Authorization', Parameter.empty()).value != parser.get("authorizeKey", "nugu"):
        raise abort(403)
    school_name = req.parameters["meal_school_name"].value
    school_data = get_school_data(req.parameters, 'meal')
    if isinstance(school_data, Response):
        if school_data.status == 404:
            response = req.get_response("school_not_found")
            return jsonify(response.to_dict())
        response = req.get_response("backend_proxy_error")
        return jsonify(response.to_dict())

    # regional_redundancy_error
    if len(school_data) > 1:
        locate = check_regional_redundancy(name=school_name, data=school_data)
        if len(locate) > 1:
            response = req.get_response("regional_redundancy_error")
            area_candidate = str()
            for i in locate.keys():
                area_candidate += f", {i} {', '.join(locate.get(i))}"

            response.set_output("area_candidate", area_candidate.replace(",", "", 1))
            return jsonify(response.to_dict())

    date_item = DateConvert.from_parameter(
        param1=req.parameters.get('meal_datetiem_1'),
        param2=req.parameters.get('meal_datetiem_2', Parameter.empty())
    )
    if date_item is None:
        return jsonify(req.get_response("date_not_found").to_dict())
    default_parameter = MultiDict([
        ('provincial', school_data[0].sc_code),
        ('code', school_data[0].sd_code),
        ('date', date_item.date.strftime('%Y%m%d'))
    ])

    result = meal_invoke(default_parameter)
    if result.status != 200:
        if result.status == 404:
            response = req.get_response("meal_not_found")
            response.set_output("datetime_format", date_item.format)
            return jsonify(response.to_dict())
        response = req.get_response("backend_proxy_error")
        return jsonify(response.to_dict())
    data = result.data['data']

    meal_type = req.parameters.get('meal_type', Parameter.empty()).value
    convert_type_name = {
        '조식': 'breakfast',
        '중식': 'lunch',
        '석식': 'dinner'
    }
    _meal_type = convert_type_name[meal_type]

    response = req.get_response("OK")
    response.set_output("datetime_format", date_item.format)
    response.set_output(
        "meal_status",
        ", ".join(data[_meal_type]['meal'])
    )
    if req.is_display:
        display = req.display
        display.badge = False
        icon = ImageObject(url="https://api.yhs.kr/school/nugu/icon")
        display.set_title(
            icon=icon,
            text="{0}의 {1} 정보".format(
                school_name,
                meal_type
            )
        )
        positive = []
        for key in ['breakfast', 'lunch', 'dinner']:
            if data[key] is not None:
                positive.append(data[key])

        if len(positive) >= 2:
            for key in convert_type_name.keys():
                value = convert_type_name[key]
                if key == meal_type:
                    continue
                display.items.append({
                    "token": display.token,
                    "header": {
                        "text": key
                    },
                    "body": {
                        "text": ", ".join(data[value]['meal'])
                    }
                })
        else:
            start_date = DateConvert.get_first_date(date_item.datetime)
            end_date = DateConvert.get_last_date(date_item.datetime)
            another_request_parameter = MultiDict([
                ('provincial', school_data[0].sc_code),
                ('code', school_data[0].sd_code),
                ('startDate', start_date.strftime('%Y%m%d')),
                ('endDate', end_date.strftime('%Y%m%d'))
            ])
            display.items.append({
                "token": display.token,
                "header": {
                    "text": DateConvert.change_weekday(date_item.date.weekday())
                },
                "body": [{
                    "text": x
                } for x in data[_meal_type]['meal']]
            })
            another_result = meal_invoke(another_request_parameter)
            if another_result.status == 200:
                another_data = {}
                for _another_data in sorted(another_result.data['data'], key=lambda x: int(x['date'])):
                    if _another_data['date'] not in data:
                        another_data[int(_another_data['date'])] = []

                    if _another_data['type'] == meal_type:
                        another_data[int(_another_data['date'])] = _another_data

                for _date in range(5):
                    _another_date = DateConvert.add_days(start_date, _date)
                    if _another_date.strftime('%Y%m%d') == date_item.date.strftime('%Y%m%d'):
                        continue
                    _another_data = another_data.get(int(_another_date.strftime('%Y%m%d')))
                    if _another_data is None:
                        display.items.append({
                            "token": display.token,
                            "header": {
                                "text": DateConvert.change_weekday(
                                    _another_date.weekday()
                                )
                            },
                            "body": [{
                                "text": "급식정보 없음."
                            }],
                            "footer": {
                                "text": "휴교 중이거나, 방학 중에는 급식 정보가 없습니다."
                            }
                        })
                        continue

                    display.items.append({
                        "token": display.token,
                        "header": {
                            "text": DateConvert.change_weekday(
                                _another_date.weekday()
                            )
                        },
                        "body": [{
                            "text": x
                        } for x in data[_meal_type]['meal']]
                    })
        response.directives.append(display.get_response(DisplayType.TextList3))
    return jsonify(response.to_dict())


@bp.route("/timetable", methods=['POST'])
def timetable_nugu():
    try:
        req = Request.from_data(request.data)
    except KeyError:
        raise abort(403)
    # print([(x, req.parameters[x].value) for x in req.parameters])

    parser = get_config()
    if req.parameters.get('Authorization', Parameter.empty()).value != parser.get("authorizeKey", "nugu"):
        raise abort(403)
    school_name = req.parameters["timetable_school_name"].value
    school_data = get_school_data(req.parameters, 'timetable')
    grade_name = req.parameters['timetable_grade']
    class_name = req.parameters['timetable_class']
    if isinstance(school_data, Response):
        if school_data.status == 404:
            response = req.get_response("school_not_found")
            return jsonify(response.to_dict())
        response = req.get_response("backend_proxy_error")
        return jsonify(response.to_dict())

    # regional_redundancy_error
    if len(school_data) > 1:
        locate = check_regional_redundancy(name=school_name, data=school_data)
        if len(locate) > 1:
            response = req.get_response("regional_redundancy_error")
            area_candidate = str()
            for i in locate.keys():
                area_candidate += f", {i} {', '.join(locate.get(i))}"

            response.set_output("area_candidate", area_candidate.replace(",", "", 1))
            return jsonify(response.to_dict())

    date_item = DateConvert.from_parameter(
        param1=req.parameters.get('timetable_datetime_1'),
        param2=req.parameters.get('timetable_datetime_2', Parameter.empty())
    )
    if date_item is None:
        return jsonify(req.get_response("date_not_found").to_dict())
    default_parameter = MultiDict([
        ('provincial', school_data[0].sc_code),
        ('code', school_data[0].sd_code),
        ('kind', ["초등학교", "중학교", "고등학교", "특수학교"].index(school_data[0].type)),
        ('grade', grade_name.value.rstrip('학년')),
        ('class', class_name.value.rstrip('반')),
        ('date', date_item.date.strftime('%Y%m%d'))  # if not req.is_test else ('date', "20211228")
    ])

    result = timetable_invoke(default_parameter)
    if result.status != 200:
        if result.status == 404:
            response = req.get_response("timetable_not_found")
            return jsonify(response.to_dict())
        response = req.get_response("backend_proxy_error")
        return jsonify(response.to_dict())
    data = result.data['data']

    response = req.get_response("OK")
    response.set_output("datetime_format", date_item.format)
    timetable = sorted(data['timetable'], key=lambda x: x['time'])
    response.set_output(
        "timetable_status",
        ", ".join(
            [x['subject'] for x in timetable]
        )
    )
    if req.is_display:
        display = req.display
        display.badge = False
        icon = ImageObject(url="https://api.yhs.kr/school/nugu/icon")
        display.set_title(
            icon=icon,
            text="{0} {1} {2}의 시간표 정보".format(
                school_name, grade_name, class_name
            )
        )
        for subject in timetable:
            display.items.append({
                "token": display.token,
                "header": {
                    "text": "{0} 교시".format(subject['time'])
                },
                "body": {
                    "text": "{0}".format(subject['subject'])
                }
            })
        response.directives.append(display.get_response(DisplayType.TextList1))
    return jsonify(response.to_dict())


def get_school_data(parameter: Dict[str, Parameter], parameter_key: str):
    school_name = parameter["{}_school_name".format(parameter_key)].value
    default_parameter = MultiDict([
        ('name', school_name),
    ])
    result = school_invoke(default_parameter, convert=False)
    if result.status != 200:
        return result
    data: List[School] = result.data['data']

    if '{0}_lcp'.format(parameter_key) in parameter:
        filtering_location = parameter['{0}_lcp'.format(parameter_key)].value
        final_result = [_school for _school in data if _school.address1.find(filtering_location) != -1]
    else:
        final_result = data
    return final_result


def check_regional_redundancy(name, data):
    location_data = []
    for _school in data:
        if _school.name.endswith(name) and len(
                _school.name.replace(name, '')
        ) > 2:
            location_data.append(_school)

    locate = {}
    for i in location_data:
        location_i = i.address1.split()
        if location_i[0] not in locate:
            locate[location_i[0]] = list()

        if location_i[1] not in locate[location_i[0]]:
            locate[location_i[0]].append(location_i[1])
    return locate
