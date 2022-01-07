from flask import Blueprint
from flask import request
from flask import abort
from flask import jsonify

from .api import meal_invoke
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
    if req.parameters.get('KEY', None).value != parser.get("authorizeKey", "nugu"):
        raise abort(403)
    data = meal_invoke(request.args)
    return jsonify(req.get_response("OK").to_dict())
