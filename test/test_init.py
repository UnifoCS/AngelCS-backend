import math
import json

import pandas as pd

from api.service.tagging_service import BaseTaggingService
from api.model.sqlalchemy import User, Channel, Review, Tag, LinkUserChannel, TemplateCondition, Template
from api import App
import api.globals as g
from configs import DefaultConfig
from configs.test import TestConfig



def test():
    app = App(TestConfig())
    tagger = BaseTaggingService()
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
    aggressive_tag = Tag(id=3, name="공격적")

    session.add(positive_tag)
    session.add(negative_tag)
    session.add(question_tag)
    session.add(aggressive_tag)
    session.commit()

    # 템플릿을 추가합니다.
    template_data_list = json.load(open("test/data/templates.json"))

    for t in template_data_list:
        app.services.template.add_template(t)

    data = pd.read_csv("test/data/google_play_sample_125.csv").sample(frac=1)
    print(data.head())

    for i in data.index:
        author = data.loc[i, 'author']
        content=data.loc[i, 'comment']
        title= content[:10] if len(content) > 10 else content 
        rating= int(data.loc[i, 'rating'])

        review = Review(
            title=title,
            author=author,
            content=content,
            rating=rating,
            channel_id=channel.id
        )
        
        result = tagger.predict(content)

        if result['is_aggressive'] > 0.5:
            review.tags.append(aggressive_tag)
        if result['sentiment'] == 'pos':
            review.tags.append(positive_tag)
        elif result['sentiment'] == 'nat':
            review.tags.append(negative_tag)
        if result['is_contact'] > 0.5:
            review.tags.append(question_tag)

        session.add(review)

    session.commit()