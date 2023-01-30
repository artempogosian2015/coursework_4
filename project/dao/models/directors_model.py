from marshmallow import Schema, fields

from project.setup.db import db
from project.setup.db import models


class Director(models.Base):
    __tablename__ = 'director'
    name = db.Column(db.String(255), unique=True, nullable=False)


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()
