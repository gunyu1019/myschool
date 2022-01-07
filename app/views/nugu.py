from flask import Blueprint
from flask import request
from .api import meal_invoke

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
    print(request.data.decode('utf8'))
    return str(meal_invoke(request.args))
