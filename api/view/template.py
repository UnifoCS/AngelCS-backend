from flask.blueprints import Blueprint
from flask import request
from . import json_api
import api.globals as g

bp = Blueprint(__name__, __name__)


@bp.route("/templates", methods=["GET", "POST"])
@json_api
def templates():
    """
     저장된 모든 템플릿 목록을 리턴하는 API
    """
    
    if request.method == "GET":
        templates = g.app.services.template.get_all_templates()
        return [x.as_dict(conditions=True) for x in templates]

    elif request.method == "POST":
        temp = request.json
        res = g.app.services.template.add_template(temp)

        return 200 if res else 400
    
@bp.route("/template/<int:id>", methods=["DELETE", "PUT"])
@json_api
def one_template(id):

    if request.method == "DELETE":
        res = g.app.services.template.delete_by_id(id)
        return 200 if res else 400

    # 템플릿 수정하기 = 지우고 다시 만들기
    elif request.method == "PUT":
        g.app.services.template.delete_by_id(id)
        temp = request.json
        res = g.app.services.template.add_template(temp)

        return 200 if res else 400