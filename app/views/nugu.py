from flask import Blueprint
from flask import request
from flask import abort
from flask import jsonify

from .api import meal_invoke
from app.models.nugu import *

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
    req = Request.from_data(request.data)

    data = meal_invoke(request.args)
    return jsonify(req.get_response("OK").to_dict())
