from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

director: Model = api.model('Режиссер', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Тим Бёртон'),
})

movie: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=255, example='Марс Атакует!'),
    'description': fields.String(required=True, max_length=255, example='...'),
    'trailer': fields.String(required=True, max_length=255, example='https://www.youtube.com/watch?v=Qjpmysz4x-4'),
    'year': fields.Integer(required=True, example=1999),
    'rating': fields.Float(required=True, example=7.2),
    'genre_id': fields.Integer(required=True, example=1),
    'genre': fields.String(attribute='genre.name', example='Комедия'),
    # 'genre': fields.Nested(genre),
    'director_id': fields.Integer(required=True, example=2),
    'director': fields.String(attribute='director.name', example='Тим Бёртон'),
})


user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, max_length=200, example='test@test.com'),
    'role': fields.String(max_length=100, example='user'),
    'name': fields.String(max_length=100, example='John'),
    'surname': fields.String(rmax_length=100, example='Smith'),
    'favorite_genre_id': fields.Integer(example=1),
    'favorite_genre': fields.String(attribute='favorite_genre.name', example='Комедия'),
})

favorite: Model = api.model('Любимое', {
    'user_id': fields.Integer(example=1),
    'user': fields.Nested(user),
    'movie_id': fields.Integer(example=2),
    'movie': fields.Nested(movie),
})

favorite_movies_old: Model = api.model('Любимые фильмы', {
     'movie': fields.Nested(movie),
})

favorite_movies: Model = api.model('Любимые фильмы', {
    'id': fields.Integer(attribute='movie.id', example=1),
    'title': fields.String(attribute='movie.title', example='Марс Атакует!'),
    'description': fields.String(attribute='movie.description', example='...'),
    'trailer': fields.String(attribute='movie.trailer', example='https://www.youtube.com/watch?v=Qjpmysz4x-4'),
    'year': fields.Integer(attribute='movie.year', example=1999),
    'rating': fields.Float(attribute='movie.rating', example=7.2),
    'genre_id': fields.Integer(attribute='movie.genre_id', example=1),
    'genre': fields.String(attribute='movie.genre.name', example='Комедия'),
    'director_id': fields.Integer(attribute='movie.director_id', example=2),
    'director': fields.String(attribute='movie.director.name', example='Тим Бёртон'),
})


favored_by: Model = api.model('Любимые фильмы', {
     'user': fields.Nested(user),
})
