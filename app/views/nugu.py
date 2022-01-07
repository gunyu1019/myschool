from flask import Blueprint
from flask import request

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
    return str(meal_invoke(request.args))
