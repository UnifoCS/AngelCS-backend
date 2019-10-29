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
        리뷰 목록을 가져옴. 
        HTTP Parameters
        - page: 가져올 페이지(1부터 시작)
        - 가져올 페이지의 크기, 기본 30
        - sort: 정렬할 기준
        - order: 정렬 순서, 기본 내림차순 (desc) 혹은 오름차순(asc)
        - filter: 기본값(모두), replied(답변 된것만), unreplied(답변 안된 것만)
    """
    page = int(request.args.get('page', '1')) - 1
    page_size = int(request.args.get('page_size', '30'))
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
    """
        특정 리뷰의 Detail을 가져오는 API
        tag, 추천 template까지 가져옴
    """
    review = g.app.services.review.get_review(id)
    result = review.as_dict()

    if review.tags:
        result["tags"] = [x.as_dict() for x in review.tags]

    templates = g.app.services.template.recommendate_templates(review)
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
    """
        리뷰에 답글을 다는 API
        Content-Type: application/json
        URL의 id는 답글을 달 리뷰의 ID,
        Body에 json으로 데이터 전송, reply에는 답글 내용을 입력.
    """
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
