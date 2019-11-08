from api import App
from api.service.review_service import ReviewService
from configs.release import ReleaseConfig
from pprint import pprint


app = App(ReleaseConfig())
gcp = app.services.gcp

# print("GCP Reviews")
# print(gcp.get_reviews())

# print("Reply")
# rid = "gp:AOqpTOHn00GOlueK3OEsm7aecZxR6DX4wEErSW43fUG2ijKzU74LFuE5739qs51GFMVq1j_qd2W7tDXf4qsWRA4"
# pprint(gcp.gcp.reviews())
# print(gcp.reply_review(rid, "감삼다 ㅎㅎ"))

gcp.load_reviews()