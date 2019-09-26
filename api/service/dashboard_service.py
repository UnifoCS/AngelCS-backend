from datetime import timedelta

from .sqlalchemy import BaseDatabaseService


class DashboardService(BaseDatabaseService):

    def get_review_count(self):
        return 2343

    def get_review_count_unreplied(self):
        return 1000

    def get_review_average_by_days(self, from_date, to_date):
        dt = from_date
        avgs = []
        rating = 3.0

        while dt < to_date:
            avgs.append({'date': dt.strftime('%Y-%m-%d'), 'rating': rating})

            rating = rating + 0.2
            dt = dt + timedelta(days=1)
        
        return avgs