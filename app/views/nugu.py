from flask import Blueprint
from flask import request
from flask import abort
from flask import jsonify
from werkzeug.datastructures import MultiDict

from .api import school_invoke, meal_invoke
from app.models.nugu import *
from app.config.config import get_config

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

    parser = get_config()
    if req.parameters.get('Authorization', Parameter.empty()).value != parser.get("authorizeKey", "nugu"):
        raise abort(403)

    print([(x, req.parameters[x].value) for x in req.parameters])
    data = meal_invoke(request.args)
    return jsonify(req.get_response("OK").to_dict())


def get_school_data(parameter: Dict[str, Parameter], parameter_key: str):
    school_name = parameter["{}_school_name".format(parameter_key)].value
    default_parameter = MultiDict([
        ('name', school_name),
    ])
    data = school_invoke(default_parameter)
    if '{0}_lcp'.format(parameter_key) in parameter:
        filtering_location = parameter['{0}_lcp'.format(parameter_key)].value
    return
