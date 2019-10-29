from collections import OrderedDict
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Index, Boolean
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from werkzeug.security import generate_password_hash, check_password_hash
from api.util.text import convert_camel_to_snake

Base = declarative_base()


class BaseModel():
    __mapper_args__= {'always_refresh': True}
    

    @declared_attr
    def __tablename__(cls):
        """
        테이블명은 Wrapper 클래스의 이름을 snake_case로 바꾸도록 만드는 함수.
        """
        return convert_camel_to_snake(cls.__name__)



class IdMixin():
    """
    이 클래스를 상속하는 래퍼 클래스는 ID 필드를 갖게됨.
    """
    id =  Column(Integer, primary_key=True, autoincrement=True)


class TimestampMixin():
    """
    이 클래스를 상속하는 래퍼 클래스는 created_date(생성시간), updated_date(마지막 변경시간) 필드를 갖게됨.
    updated_date는 레코드의 다른 값이 바뀌면 바로 변경됨.
    """
    created_date = Column(DateTime, default=datetime.utcnow())
    updated_date = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())



class User(Base, BaseModel, IdMixin, TimestampMixin):
    """
    AngelCS를 사용하는 유저를 나타내는 테이블.
    """
    name = Column(String(32), nullable=False)
    email = Column(String(64), nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)

    # get channels of this user
    channels = relationship('Channel', secondary='link_user_channel')

    #below our user model, we will create our hashing functions
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def as_dict(self, channels=False):
        d = {
            'id': self.id,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat(),
            'name': self.name,
            'email': self.email
        }
        if channels:
            d['channels'] = [x.as_dict() for x in self.channels]
        return d


class ReferenceUserMixin:
    """
    한 유저에 종속되어 1-to-many관계를 갖는 테이블을 위한 믹스인 클래스
    """
    @declared_attr
    def user_id(cls):
        return Column(Integer, ForeignKey("user.id"), index=True, nullable=False)


class Channel(Base, BaseModel, IdMixin, TimestampMixin):
    """
    채널은 유저가 리뷰를 가져오는 곳을 의미함(유튜브, 플레이스토어, 쿠팡 등)
    """
    name = Column(String(64), nullable=False)
    provider = Column(String(64), nullable=False)

    # get all templates of user's specific template
    # templates = relationship("Template", backref="template")

    # get all users who has this channel
    users = relationship('User', secondary='link_user_channel')

    # get all reviews of this channel
    reviews = relationship("Review", backref="channel")

    def as_dict(self):
        return {
            'id': self.id,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat(),
            'name': self.name,
            'provider': self.provider
        }


class ReferenceChannelMixin():
    """
    하나의 채널에 종속된 1-to-many를 나타내기 위한 믹스인 클래스.
    """
    @declared_attr
    def channel_id(cls):
        return Column(Integer, ForeignKey("channel.id"), index=True, nullable=False)


class LinkUserChannel(Base, BaseModel, IdMixin):
    """
    유저와 채널간의 many-to-many 관계를 표현하기 위한 클래스.
    """
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    channel_id = Column(Integer, ForeignKey('channel.id'), nullable=False)
    __table_args__ = (
        Index('index_user_channel_id', user_id, channel_id, unique=True),
    )


class Review(Base, BaseModel, IdMixin, TimestampMixin, ReferenceChannelMixin):
    """
    리뷰 테이블을 나타내는 클래스로, 하나의 채널에 종속된다.
    """
    title = Column(String(64), nullable=False)
    author = Column(String(32), nullable=False)
    content = Column(String(1024), nullable=False)
    rating = Column(Integer, nullable=False, index=True)
    
    is_replied = Column(Boolean, nullable=False, index=True, default=False)
    is_aggressive = Column(Boolean, nullable=False, index=True, default=False)
    reply = Column(String)

    # get tags of this review
    tags = relationship('Tag', secondary='link_review_tag')

    def as_dict(self, tags=False):
        d = {
            'id': self.id,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat(),
            'title': self.title,
            'author': self.author,
            'content': self.content,
            'rating': self.rating,
            'is_replied': self.is_replied,
            'reply': self.reply,
            'is_aggressive': self.is_aggressive
        }
        if tags:
            d['tags'] = [x.as_dict() for x in self.tags]
        return d

class ReferenceReviewMixin():
    """
    하나의 리뷰에 종속되어 1-to-many관계를 갖는 클래스를 위한 믹스인 클래스.
    """
    @declared_attr
    def review_id(cls):
        return Column(Integer, ForeignKey("review.id"), index=True)



class Tag(Base, BaseModel, IdMixin, TimestampMixin):
    """
    리뷰의 태그를 나타내는 클래스. 
    Review와 many-to-many관계를 가짐.
    """
    name = Column(String(32), nullable=False)
    
    reviews = relationship('Tag', secondary='link_review_tag')

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class LinkReviewTag(Base, BaseModel, IdMixin):
    """
    SQLAlchemy에서 리뷰와 태그를 many-to-many로 연결하기 위한 클래스
    """
    review_id = Column(Integer, ForeignKey('review.id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tag.id'), nullable=False)

    __table_args__ = (
        Index('index_link_review_tag', review_id, tag_id, unique=True),
    )



class Template(Base, BaseModel, IdMixin, TimestampMixin, ReferenceChannelMixin):
    """
    템플릿 테이블을 나타내기 위한 클래스. 
    0개 이상의 TemplateCondition을 가짐.
    """
    name = Column(String(32), nullable=False)
    content = Column(String, nullable=False)

    conditions = relationship("TemplateCondition", backref="template", cascade="all, delete-orphan")


    def as_dict(self, conditions=False):
        d = {
            'id': self.id,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat(),
            'name': self.name,
            'content': self.content
        }
        if conditions:
            d['conditions'] = [x.as_dict() for x in self.conditions]
        return d

class ReferenceTemplateMixin():
    """
    하나의 템플릿에 종속되어 1-to-many관계를 가진 테이블을 나타내기위한 믹스인 클래스.
    """

    @declared_attr
    def template_id(cls):
        return Column(Integer, ForeignKey("template.id"), index=True, nullable=False)

class TemplateCondition(Base, BaseModel, IdMixin, ReferenceTemplateMixin):
    """
    Template이 리뷰에 적용되기 위한 조건이 나열된 클래스.
    TemplateCondition은 하나의 template에 여러개가 연결된 1-to-many
    """
    index = Column(Integer, index=True)
    operand1 = Column(String)
    operand2 = Column(String)
    operator = Column(String(16), nullable=False)

    def as_dict(self, conditions=False):
        d = {
            'id': self.id,
            'index': self.index,
            'operand1': self.operand1,
            'operand2': self.operand2,
            'operator': self.operator
        }
        return d
