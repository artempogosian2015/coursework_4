from flask import request, abort
from flask_restx import Namespace, Resource

from project.container import user_service

api = Namespace('auth')


@api.route('/register')
class AuthRegisterView(Resource):
    def post(self):
        user = request.json
        username = user.get('email', None)
        password = user.get('password', None)

        if None in [username, password]:
            abort(400)

        user_service.create(user)
        return "", 201


@api.route('/login')
class AuthLoginView(Resource):
    def post(self):
        user = request.json
        username = user.get('email', None)
        password = user.get('password', None)

        if None in [username, password]:
            abort(400)

        if result := user_service.create_tokens(username, password):
            return result

        return {"error": f"Неверные учётные данные. User: {username}, pass: {password}"}, 401

    def put(self):
        req_json = request.json
        refresh_token = req_json.get('refresh_token', None)
        if refresh_token is None:
            abort(400)

        if result := user_service.refresh_tokens(refresh_token):
            return result

        abort(400)

