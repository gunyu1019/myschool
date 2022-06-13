import datetime
import json

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
from app.models.assistant import Request
from app.module.school import School

bp = Blueprint(
    name="google_assistant_backend",
    import_name="google_assistant_backend",
    url_prefix="/school"
)


@bp.route("/google.assistant", methods=['GET', 'POST'])
def webhook_event():
    pre_data = json.loads(
        request.data.decode('utf8')
    )
    # print(json.dumps(pre_data, indent=4))
    data = Request(pre_data)
    # print(data)
    if data.handler == "school_search":
        return
    return

