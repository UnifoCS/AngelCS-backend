import api.globals as g
from flask import request, Response
from flask.blueprints import Blueprint
import random

from . import json_api

bp = Blueprint(__name__, __name__)


@bp.route("/reviews")
@json_api
def get_review_list():
    """
    # 결과 예시
    for i in range(1, 30):
        item = {
            "id": i, # Review ID(int)
            "author": f"Test-{i}", # 리뷰 작성자 이름(string)
            "score": random.random() * 5, # 점수(int)
            "updated_at": "2019-01-11", # (date, yyyy-MM-dd) 리뷰 변경일(변경하지 않았을 경우 created_at과 동일한 값)
            "created_at": "2019-01-11", # (date, yyyy-MM-dd) 리뷰 작성일
            "is_replied": False, # (boolean) 이미 답변이 달렸는가
            "tags": [ # 태그 목록, 없으면 빈 목록
                { "id": 1234, "name": "긍정" },
                { "id": 1235, "name": "질문" }
            ]
        }
        items.append(item)
    """
    page = (int(request.args.get('page')) or 1) - 1
    page_size = int(request.args.get('page_size')) or 30
    sort = request.args.get('sort', 'updated_date')
    order = request.args.get('order', 'desc')
    filter = request.args.get('filter', None)

    items = g.app.services.review.get_review_list(
        index=page * page_size,
        count=page_size,
        sort=sort,
        order=order,
        filter=filter
    )
    result = [x.as_dict(tags=True) for x in items]

    return result


@bp.route("/review/<int:id>")
@json_api
def get_review(id):
    # TODO: Not implemented
    review = g.app.services.review.get_review(id)
    result = review.as_dict()

    if review.tags:
        result["tags"] = [x.as_dict() for x in review.tags]

    templates = g.app.services.template.get_template_by_tags(review.tags)
    if templates:
        result["recommended_templates"] = [x.as_dict(conditions=True) for x in templates]

    return result

    # return {
    #     "id": id, # 리뷰 ID(int)
    #     "author": f"Test-{id}", # 리뷰 작성자 이름(string)
    #     "content": "리뷰 내용", # 리뷰 내용(string)
    #     "score": random.random() * 5, # 점수(int)
    #     "updated_at": "2019-01-11", # (date, yyyy-MM-dd) 리뷰 변경일(변경하지 않았을 경우 created_at과 동일한 값)
    #     "created_at": "2019-01-11", # (date, yyyy-MM-dd) 리뷰 작성일
    #     "is_replied": False, # (boolean) 이미 답변이 달렸는가
    #     "reply_text": None, # (string, nullable) 이미 답변이 달렸으면 
    #     "tags": [ # 태그 목록, 없으면 빈 목록
    #         { "id": 1234, "name": "긍정" }, # 태그ID, 태그이름
    #         { "id": 1235, "name": "질문" }
    #     ],
    #     "recommended_templates" : [ # 이 리뷰에 자동으로 추천된 답글 템플릿
    #         {
    #             "id": 123, # (int) 템플릿 ID
    #             "name": "악플러용", # 제목
    #             "content": "안녕하세요 [name]님. ...", # 내용
    #             "conditions": [ # 템플릿이 적용되기 위한 조건
    #                 { "type": "tag", "tag_id": 1234 }, 
    #                 { "type": "score", "operator": "<=", "operand": 3 } 
    #             ]
    #         }
    #     ]
    # }


@bp.route("/review/<int:id>/reply", methods=["POST"])
@json_api
def reply_review(id):
    params = request.json
    reply = params['reply']

    if not reply:
        return {"message": "You must put reply content in the request"}, 400

    changed = g.app.services.review.reply_review(id, reply)
    if changed:
        return ("", 200)  
    else: 
        e = {
            "message": f"Could not find review."
        }
        return e, 404
