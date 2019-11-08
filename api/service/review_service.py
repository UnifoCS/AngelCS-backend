from .sqlalchemy_service import BaseDatabaseService
from ..model.sqlalchemy import Review
import requests
import json


class ReviewService(BaseDatabaseService):
    """
    리뷰와 관련된 기능을 제공하는 서비스
    - 리뷰 검색
    - 리뷰 가져오기
    - 리뷰 삭제, 추가 등
    - 리뷰에 답글 달기
    - 리뷰 분석

    """
    
    
    def get_review(self, id):
        return self.query(Review).filter_by(id=id).first()

    def get_review_list(self, channel_id="", count=10, index=None, sort='updated_date', order='desc', filter=None):
        q = self.query(Review)
        
        if filter == "replied":
            q = q.filter_by(is_replied=True)
        elif filter == "unreplied":
            q = q.filter_by(is_replied=False)

        if sort in ('updated_date', 'created_date', 'rating') and hasattr(Review, sort):
            column = getattr(Review, sort)
            if order == "desc":
                q = q.order_by(column.desc())
            else:
                q = q.order_by(column.asc())

        if count:
            q = q.limit(count)
        if index:
            q = q.offset(index)
        
        return q.all()

    def reply_review(self, id, reply):
        r = self.get_review(id)
        if r:
            r.is_replied = True
            r.reply = reply
            self.commit()

            if r.rid:
                self.app.services.gcp.reply_review(r.rid, reply)
                
            return True
        else:
            return False

