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
    
    def load_from_google_play(self):
        pkg = ""
        access_token = ""
        url = f"https://www.googleapis.com/androidpublisher/v3/applications/{pkg}/reviews?access_token={access_token}&maxResults=100"

        res = requests.get(url)
        if int(res.status_code / 100) == 2:
            result = json.loads(res.text)
            reviews = result['reviews']

            models = []
            for review in reviews:
                model = Review()
                model.id = int(review['id'])
                model.author = review['authorName']

                for comment in review['comments']:
                    
                    if "userComment" in comment:
                        model.title = comment['text']
                        model.content = comment['text']
                        model.rating = comment['starRating']

                    if "developerComment" in comment:
                        model.is_replied = True
                        model.reply = comment['text']

                models.append(model)

            # insert loaded models
            self.session.add_all(models)
            self.session.commit()
            
            return True
        else:
            return False

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
            return True
        else:
            return False

    def reply_google_play(self, id, reply_text):
        access_token = ""
        pkg = ""
        url = f"https://www.googleapis.com/androidpublisher/v3/applications/{pkg}/reviews/" + \
                f"{id}:reply?access_token={access_token}"

        content = {
            "replyText": reply_text
        }

        res = requests.post(url, json=content)

        return int(res.status_code / 100) == 2
