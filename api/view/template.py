from flask.blueprints import Blueprint

from . import json_api
import api.globals as g

bp = Blueprint(__name__, __name__)


@bp.route("/templates")
@json_api
def get_templates():
    """
    return [
        {
            "id": 123, # (int) 템플릿 ID
            "name": "악플러용", # 제목
            "content": "안녕하세요 [name]님. ...", # 내용
            "conditions": [ # 템플릿이 적용되기 위한 조건
                { "type": "tag", "tag_id": 1234 }, 
                { "type": "score", "operator": ">=", "operand": 3 } 
            ]
        }
    ]
    """
    
    templates = g.app.services.template.get_all_templates()
    return [x.as_dict(conditions=True) for x in templates]

    