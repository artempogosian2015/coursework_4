from flask import request, abort, jsonify
from flask_restx import Namespace, Resource

from project.container import favorite_service, movie_service
from project.exceptions import DuplicateItem
from project.setup.api.models import favorite, favorite_movies, favored_by, user, movie
from project.views.decorators import auth_returned

api = Namespace('favorites')

@api.route('/movies/<int:mid>')
class AddFavoriteMovie(Resource):

    @auth_returned
    def post(self, mid, obj=None):
        if not obj:
            abort(400)

        uid = obj['id']

        if movie_service.get_one(mid) is None:
            abort(400)

        if favorite_service.create(uid, mid):
            return "", 201

        raise DuplicateItem('Already exists')

    @auth_returned
    def delete(self, mid, obj=None):
        if not obj:
            abort(400)

        if movie_service.get_one(mid) is None:
            abort(400)

        uid = obj['id']
        favorite_service.delete(uid, mid)
        return "", 204

    @api.marshal_with(user, code=200, description='OK')
    def get(self, mid):
        return favorite_service.get_users(mid)

@api.route('/users/<int:uid>')
class GetFavoriteMovie(Resource):
    @api.marshal_with(movie, code=200, description='OK')
    def get(self, uid):
        return favorite_service.get_movies(uid)



