from .sqlalchemy import BaseDatabaseService


class ReviewService(BaseDatabaseService):

    def get_review(self, id):
        pass

    def get_review_list(self, count, index):
        pass

    def reply_review(self, id, reply):
        pass

