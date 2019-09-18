from flask.blueprints import Blueprint
from flask import jsonify

from . import json_api

bp = Blueprint(__name__, __name__)


@bp.route("/dashboard")
@json_api
def get_dashboard():
    return [
        {
            "type": "review_count", 
            "item": {
                "review_total_count": 10000,
                "review_replied_count": 1000,
            }
        },
        {
            "type": "review_average",
            "item": {
                "review_average_score": 3.5, # 리뷰 평균
                "review_average_history": [ # 리뷰 내역
                    { "date": "yyyy-MM-dd", "score": 3.5  },
                    { "date": "yyyy-MM-dd", "score": 3.4  },
                    { "date": "yyyy-MM-dd", "score": 3.3  },
                    { "date": "yyyy-MM-dd", "score": 3.2  },
                    { "date": "yyyy-MM-dd", "score": 3.1  }
                ]
            }
        }
    ], 200