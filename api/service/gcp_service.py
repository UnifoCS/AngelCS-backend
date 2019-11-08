from google.oauth2 import service_account
import googleapiclient

from . import BaseService
from .sqlalchemy_service import BaseDatabaseService
from api.model.sqlalchemy import Review, Tag, Channel


# https://stackoverflow.com/questions/48694000/google-play-developer-api-not-returning-reviews

class GCPService(BaseDatabaseService):

    def __init__(self, app):
        super().__init__(app)

        SCOPES = ['https://www.googleapis.com/auth/androidpublisher']
        SERVICE_ACCOUNT_FILE = 'tmp/gcp.json'

        self.credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        self.gcp = googleapiclient.discovery.build('androidpublisher','v3', credentials=self.credentials)

    def get_reviews(self):
        pkg = self.app.config["GPC_APP_ID"]
        return self.gcp.reviews().list(packageName=pkg).execute()

    def load_reviews(self):
        reviews = self.get_reviews()
        reviews = reviews.get('reviews', None)

        channel = self.query(Channel).first()
        positive_tag = self.query(Tag).filter_by(id=0).first()
        negative_tag = self.query(Tag).filter_by(id=1).first()
        question_tag = self.query(Tag).filter_by(id=2).first()
        aggressive_tag = self.query(Tag).filter_by(id=3).first()

        tagger = self.app.services.tagging

        if not reviews:
            return False

        models = []
        for review in reviews:
            model = Review()
            model.channel_id = channel.id
            model.rid = review['reviewId']
            model.author = review['authorName']

            rating = 1
            for comment in review['comments']:
                
                if "userComment" in comment:
                    uc = comment['userComment']
                    c = uc['text']
                    model.title = c if len(c) <= 32 else c[:32]
                    model.content = uc['text']
                    model.rating = uc['starRating']
                    rating = model.rating

                if "developerComment" in comment:
                    dc = comment['developerComment']
                    model.is_replied = True
                    model.reply = dc['text']

            if model.content:
                result = tagger.predict(model.content)
                print("Predict Real Review: ", result)

                if rating == 1 and result['is_aggressive'] > 0.5:
                    model.tags.append(aggressive_tag)
                    model.is_aggressive = True
                if result['sentiment'] == 'pos':
                    model.tags.append(positive_tag)
                elif result['sentiment'] == 'neg':
                    model.tags.append(negative_tag)
                if result['is_contact'] > 0.8:
                    model.tags.append(question_tag)

            models.append(model)

        # insert loaded models
        self.db.add_all(models)
        self.db.commit()
        
        return True

    def reply_review(self, id, text):
        pkg = self.app.config["GPC_APP_ID"]
        body = {
            "replyText": text
        }
        return self.gcp.reviews().reply(packageName=pkg, reviewId=id, body=body).execute()