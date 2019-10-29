from datetime import timedelta

from sqlalchemy import func

from .sqlalchemy_service import BaseDatabaseService
from ..model.sqlalchemy import Review


class DashboardService(BaseDatabaseService):
    """
        대시보드와 관련된 기능을 수행하는 클래스
        - 대시보드 통계 분석 및 저장.
        - 대시보드 통계 Export
    """


    def get_review_count(self):
        return self.query(func.count(Review.id)).scalar()

    def get_review_count_unreplied(self):
        return self.query(func.count(Review.id)).filter_by(is_replied=False).scalar()

    def get_recent_reviews(self, count=5):
        return self.query(Review).order_by(Review.created_date.desc()).limit(count).all()

    def get_review_average_by_days(self, from_date, to_date):
        dt = from_date
        avgs = []
        rating = 3.0

        while dt < to_date:
            avgs.append({'date': dt.strftime('%Y-%m-%d'), 'rating': rating})

            rating = rating + 0.2
            dt = dt + timedelta(days=1)
        
        return avgs