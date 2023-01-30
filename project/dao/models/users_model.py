from marshmallow import Schema, fields

from project.dao.models.genres_model import GenreSchema
from project.setup.db import db
from project.setup.db import models


class User(models.Base):
    __tablename__ = 'user'
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(100), default='user')
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    favorite_genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    favorite_genre = db.relationship("Genre", lazy='subquery')


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    password = fields.Str()
    role = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    favorite_genre_id = fields.Int()
    favorite_genre = fields.Pluck(GenreSchema, 'name')

