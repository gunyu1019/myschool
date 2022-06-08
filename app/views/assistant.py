import datetime

from flask import Blueprint
from flask import request
from flask import abort
from flask import jsonify
from flask import send_file
from typing import List
from werkzeug.datastructures import MultiDict

from .api import school_invoke, meal_invoke, timetable_invoke
from app.config.config import get_config
from app.directory import directory
from app.response import Response
from app.module.school import School

bp = Blueprint(
    name="google_assistant_backend",
    import_name="google_assistant_backend",
    url_prefix="/school"
)


@bp.route("/google.assistant", methods=['GET', 'POST'])
def webhook_event():
    print("Headers: ", request.headers.__dict__)
    print("Data: ", request.data.decode('utf8'))
    return 'OK'

