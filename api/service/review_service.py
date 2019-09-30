from .sqlalchemy_service import BaseDatabaseService
from ..model.sqlalchemy import Review


class ReviewService(BaseDatabaseService):

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

