import math
from api.model.sqlalchemy import User, Channel, Review, Tag, LinkUserChannel, TemplateCondition, Template
from api import App
from configs import DefaultConfig

import pandas as pd
import sklearn


def test():
    app = App(DefaultConfig())
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
    positive_tag = Tag(name="긍정")
    negative_tag = Tag(name="부정")

    session.add(positive_tag)
    session.add(negative_tag)
    session.commit()

    # 템플릿을 추가합니다.
    positive_temp = Template(name="감사 리뷰 템플릿", content="Thank you [name], We will keep doing our best :)", channel_id=channel.id)
    positive_temp_cond = TemplateCondition(index=0, operand1="tag", operator="=", operand2=f"{positive_tag.id}")
    positive_temp.conditions.append(positive_temp_cond)

    negative_temp = Template(name="사과 리뷰 템플릿", content="Sorry [name], We will try more for better service.", channel_id=channel.id)
    negative_temp_cond = TemplateCondition(index=0, operand1="tag", operator="=", operand2=f"{negative_tag.id}")
    negative_temp.conditions.append(negative_temp_cond)

    session.add_all([
        positive_temp,
        negative_temp
    ])
    session.commit()


    data = pd.read_csv("test/data/samples.csv")
    data = sklearn.utils.shuffle(data)

    for i in data.index:
        title=data.loc[i, 'Title']
        content=data.loc[i, 'Text']
        rating=data.loc[i, 'Rating']

        if math.isnan(rating) or \
            (type(title) is float and math.isnan(title)) \
                or (type(content) is float and math.isnan(content)):
            continue

        review = Review(
            title=title,
            content=content,
            rating=rating,
            channel_id=channel.id
        )
        sentiment = data.loc[i, 'sum']
        review.is_aggressive = data.loc[i, '욕설여부'] == '욕설'

        if sentiment >= 0.5:
            review.tags.append(positive_tag)
        elif sentiment <= 0.5:
            review.tags.append(negative_tag)

        session.add(review)

    session.commit()