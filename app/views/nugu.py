from flask import Blueprint
from flask import request
from flask import abort
from flask import jsonify
from typing import List
from werkzeug.datastructures import MultiDict

from .api import school_invoke, meal_invoke
from app.models.nugu import *
from app.config.config import get_config
from app.module.school import School

bp = Blueprint(
    name="nugu_backend",
    import_name="nugu_backend",
    url_prefix="/nugu"
)


@bp.route("/health", methods=['GET'])
def health():
    return 'OK'


@bp.route("/meal", methods=['POST'])
def school():
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

    # regional_redundancy_error
    if len(school_data) > 1:
        location_data = []
        for _school in school_data:
            if _school.name.endswith(school_name) and len(
                _school.name.replace(school_name, '')
            ) > 2:
                location_data.append(_school)

        locate = {}
        for i in location_data:
            location_i = i.address1.split()
            if location_i[0] not in locate:
                locate[location_i[0]] = list()

            if location_i[1] not in locate[location_i[0]]:
                locate[location_i[0]].append(location_i[1])

        if len(locate) > 1:
            response = req.get_response("regional_redundancy_error")
            area_candidate = str()
            for i in locate.keys():
                area_candidate += f", {i} {', '.join(locate.get(i))}"

            response.set_output("area_candidate", area_candidate.replace(",", "", 1))
            return jsonify(response.to_dict())
    data = meal_invoke(request.args)
    return jsonify(req.get_response("OK").to_dict())


def get_school_data(parameter: Dict[str, Parameter], parameter_key: str):
    school_name = parameter["{}_school_name".format(parameter_key)].value
    default_parameter = MultiDict([
        ('name', school_name),
    ])
    result = school_invoke(default_parameter, convert=False)
    if result.status != 200:
        return
    data: List[School] = result.data['data']

    if '{0}_lcp'.format(parameter_key) in parameter:
        filtering_location = parameter['{0}_lcp'.format(parameter_key)].value
        final_result = [_school for _school in data if _school.address1.find(filtering_location) != -1]
    else:
        final_result = data
    return final_result
