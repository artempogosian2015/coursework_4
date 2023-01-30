from marshmallow import Schema, fields

from project.setup.db import db
from project.dao.models.genres_model import GenreSchema
from project.dao.models.directors_model import DirectorSchema
from project.setup.db import models


class Movie(models.Base):
    __tablename__ = 'movie'
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    genre = fields.Pluck(GenreSchema, 'name')
    director_id = fields.Int()
    director = fields.Pluck(DirectorSchema, 'name')

