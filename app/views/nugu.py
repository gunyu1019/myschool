from flask import Blueprint
from .api import meal

bp = Blueprint(
    name="nugu_backend",
    import_name="nugu_backend",
    url_prefix="/nugu"
)


@bp.route("/meal", methods=['GET'])
def school():
    return meal()
