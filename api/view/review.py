import api.globals as g
from flask.blueprints import Blueprint
import random

from . import json_api

bp = Blueprint(__name__, __name__)


@bp.route("/reviews")
@json_api
def get_review_list():
    # TODO: Not implemented
    items = g.app.services.review.get_review_list()
    # for i in range(1, 30):
    #     item = {
    #         "id": i, # Review ID(int)
    #         "author": f"Test-{i}", # 리뷰 작성자 이름(string)
    #         "score": random.random() * 5, # 점수(int)
    #         "updated_at": "2019-01-11", # (date, yyyy-MM-dd) 리뷰 변경일(변경하지 않았을 경우 created_at과 동일한 값)
    #         "created_at": "2019-01-11", # (date, yyyy-MM-dd) 리뷰 작성일
    #         "is_replied": False, # (boolean) 이미 답변이 달렸는가
    #         "tags": [ # 태그 목록, 없으면 빈 목록
    #             { "id": 1234, "name": "긍정" },
    #             { "id": 1235, "name": "질문" }
    #         ]
    #     }
    #     items.append(item)

    # items = [ x.__dict__ for x in items ]
    # print(items)
    return items


@bp.route("/review/<int:id>")
@json_api
def get_review(id):
    # TODO: Not implemented

    return {
        "id": id, # 리뷰 ID(int)
        "author": f"Test-{id}", # 리뷰 작성자 이름(string)
        "content": "리뷰 내용", # 리뷰 내용(string)
        "score": random.random() * 5, # 점수(int)
        "updated_at": "2019-01-11", # (date, yyyy-MM-dd) 리뷰 변경일(변경하지 않았을 경우 created_at과 동일한 값)
        "created_at": "2019-01-11", # (date, yyyy-MM-dd) 리뷰 작성일
        "is_replied": False, # (boolean) 이미 답변이 달렸는가
        "reply_text": None, # (string, nullable) 이미 답변이 달렸으면 
        "tags": [ # 태그 목록, 없으면 빈 목록
            { "id": 1234, "name": "긍정" }, # 태그ID, 태그이름
            { "id": 1235, "name": "질문" }
        ],
        "recommended_templates" : [ # 이 리뷰에 자동으로 추천된 답글 템플릿
            {
                "id": 123, # (int) 템플릿 ID
                "name": "악플러용", # 제목
                "content": "안녕하세요 [name]님. ...", # 내용
                "conditions": [ # 템플릿이 적용되기 위한 조건
                    { "type": "tag", "tag_id": 1234 }, 
                    { "type": "score", "operator": "<=", "operand": 3 } 
                ]
            }
        ]
    }


@bp.route("/review/<int:id>/reply", methods=["POST"])
@json_api
def reply_review(id):
    return None, 200
