from flask.blueprints import Blueprint

from . import json_api
import api.globals as g

bp = Blueprint(__name__, __name__)


@bp.route("/templates")
@json_api
def get_templates():
    """
     저장된 모든 템플릿 목록을 리턴하는 API
    """
    
    templates = g.app.services.template.get_all_templates()
    return [x.as_dict(conditions=True) for x in templates]

    