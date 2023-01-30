from project.setup.db import db
from sqlalchemy import DateTime, func


class Favorite(db.Model):
    __tablename__ = 'favorite'
    created = db.Column(DateTime, nullable=False, default=func.now())
    updated = db.Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    user = db.relationship("User")
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), primary_key=True)
    movie = db.relationship("Movie")
