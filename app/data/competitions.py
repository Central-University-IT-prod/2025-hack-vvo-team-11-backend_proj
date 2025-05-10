import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Comps(SqlAlchemyBase):
    __tablename__ = 'competitions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    prize = sqlalchemy.Column(sqlalchemy.String)
    participantsCount = sqlalchemy.Column(sqlalchemy.String)
    place = sqlalchemy.Column(sqlalchemy.String)
    sport = sqlalchemy.Column(sqlalchemy.String)

    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }