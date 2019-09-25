import os,sys,inspect, math
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from api.model.sqlalchemy import User, Channel, Review, Tag, LinkUserChannel
from api import App

import pandas as pd


app = App()
sql_alchemy = app.services.sql_alchemy
session = sql_alchemy.session

# DB 초기화
sql_alchemy.drop_db()
sql_alchemy.create_db()

# 기본 유저와 채널 추가
user = User(name="HeegyuKim", email="heekue83@gmail.com")
user.set_password("test")
channel = Channel(name="Amazon Review", provider="Amazon Corp.")
link = LinkUserChannel(user_id=user.id, channel_id=channel.id)

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


data = pd.read_csv("test/data/sentiments.csv")
for i in data.index:
    title=data.loc[i, 'reviews.title']
    content=data.loc[i, 'reviews.text']
    rating=data.loc[i, 'reviews.rating']

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
    sentiment = data.loc[i, 'sentiment']

    if sentiment >= 0.5:
        review.tags.append(positive_tag)
    elif sentiment <= 0.5:
        review.tags.append(negative_tag)

    session.add(review)
    
session.commit()