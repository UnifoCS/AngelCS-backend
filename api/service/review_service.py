from .sqlalchemy import BaseDatabaseService
from ..model.sqlalchemy import Review


class ReviewService(BaseDatabaseService):

    def get_review(self, id):
        return self.query(Review).filter(id=id).first()

    def get_review_list(self, channel_id="", count=10, index=None):
        q = self.query(Review.id, Review.title, Review.content, Review.rating, Review.tags)
        
        if count:
            q = q.limit(count)
        if index:
            q = q.offset(index)
        
        return q.all()

    def reply_review(self, id, reply):
        pass

