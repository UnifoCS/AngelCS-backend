from datetime import datetime, timedelta

from flask.blueprints import Blueprint
from flask import jsonify

import api.globals as g
from . import json_api

bp = Blueprint(__name__, __name__)


@bp.route("/dashboard")
@json_api
def get_dashboard():
    """
    대시보드 정보를 리턴하는 API
    """
    dashboard = g.app.services.dashboard
    to_date = datetime.today() + timedelta(days=1)
    from_date = to_date - timedelta(days=5)

    return [
        {
            "type": "review_count", 
            "item": {
                "review_total_count": dashboard.get_review_count(),
                "review_replied_count": dashboard.get_review_count_unreplied(),
            }
        },
        {
            "type": "review_average",
            "item": {
                "review_average_score": 3.5, # 리뷰 평균
                "review_average_history": dashboard.get_review_average_by_days(from_date, to_date)
                # "review_average_history": [ # 리뷰 내역
                    # { "date": "yyyy-MM-dd", "score": 3.5  },
                    # { "date": "yyyy-MM-dd", "score": 3.4  },
                    # { "date": "yyyy-MM-dd", "score": 3.3  },
                    # { "date": "yyyy-MM-dd", "score": 3.2  },
                    # { "date": "yyyy-MM-dd", "score": 3.1  }
                # ]
            }
        }
    ], 200