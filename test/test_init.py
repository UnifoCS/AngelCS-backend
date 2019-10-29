import math
import pandas as pd

from api.model.sqlalchemy import User, Channel, Review, Tag, LinkUserChannel, TemplateCondition, Template
from api import App
import api.globals as g
from configs import DefaultConfig
from configs.debug import DebugConfig



def test():
    app = App(DebugConfig())
    sql_alchemy = app.services.sql_alchemy
    session = sql_alchemy.session

    # DB 초기화
    sql_alchemy.drop_db()
    sql_alchemy.create_db()

    # 기본 유저와 채널 추가
    user = User(name="HeegyuKim", email="heekue83@gmail.com")
    user.set_password("test")
    channel = Channel(name="Amazon Review", provider="Amazon Corp.")

    session.add(user)
    session.add(channel)
    session.commit()

    user.channels.append(channel)
    session.commit()

    # 긍정, 부정 태그를 추가합니다.
    positive_tag = Tag(id=0, name="긍정")
    negative_tag = Tag(id=1, name="부정")
    question_tag = Tag(id=2, name="문의")

    session.add(positive_tag)
    session.add(negative_tag)
    session.commit()

    # 템플릿을 추가합니다.
    template_data_list = [
        {
            "title": "감사답글 - 5점 긍정",
            "content": "[name]님 감사합니다.\n앞으로도 좋은 서비스 이어나가겠습니다.",
            "conditions": {
                "tags": [0],
                "rating": "=5"
            }
        },
        {
            "title": "감사답글 - 5점 미만 긍정",
            "content": "[name]님 감사합니다.\n앞으로도 좋은 서비스 이어나가겠습니다. 별점도 5점 주시면 감사하겠습니다.",
            "conditions": {
                "tags": [0],
                "rating": "<5"
            }
        },
        {
            "title": "사과답글 - 5점 부정",
            "content": "[name]님 안녕하세요.\n서비스의 불만족스러운 부분을 개선하기위해 노력하겠습니다.\n감사합니다.",
            "conditions": {
                "tags": [1],
                "rating": "=5"
            }
        },
        {
            "title": "사과답글 - 1점 부정",
            "content": "[name]님 안녕하세요.\n서비스의 불만족스러운 부분을 개선하기위해 노력하겠습니다. 별점도 5점 주시면 저희가 개발하는데 힘이 날 것 같습니다.\n감사합니다.",
            "conditions": {
                "tags": [1],
                "rating": "<5"
            }
        },
        {
            "title": "문의답글 - 5점",
            "content": "[name]님 안녕하세요.\n문의해주신 내용 접수하였습니다.\n\n\n감사합니다.",
            "conditions": {
                "tags": [2],
                "rating": "=5"
            }
        },
        {
            "title": "문의답글 - 5점",
            "content": "[name]님 안녕하세요.\n문의해주신 내용 접수하였습니다.\n\n\n별점 5점 부탁드립니다. 감사합니다.",
            "conditions": {
                "tags": [2],
                "rating": "<5"
            }
        }
    ]

    for t in template_data_list:
        app.services.template.add_template(t)

    data = pd.read_csv("test/data/samples.csv").sample(frac=1)
    print(data)

    for i in data.index:
        title=data.loc[i, 'Title']
        author = data.loc[i, 'Author']
        content=data.loc[i, 'Text']
        rating=int(data.loc[i, 'Rating'])

        print(rating)

        if math.isnan(rating) or \
            (type(title) is float and math.isnan(title)) \
                or (type(content) is float and math.isnan(content)):
            continue

        review = Review(
            title=title,
            author=author,
            content=content,
            rating=rating,
            channel_id=channel.id
        )
        sentiment = data.loc[i, 'pos/neg 예측']
        review.is_aggressive = data.loc[i, '욕설여부'] == '욕설'

        if sentiment == '긍정':
            review.tags.append(positive_tag)
        elif sentiment == '부정':
            review.tags.append(negative_tag)
        
        if '?' in review.content or '?' in review.title:
            review.tags.append(question_tag)

        session.add(review)

    session.commit()