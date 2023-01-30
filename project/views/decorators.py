from functools import wraps

import jwt
from flask import request, abort

from project.config import config


def auth_required(func):

    @wraps(func)
    def __wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        try:
            jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM,])
        except Exception as e:
            abort(401)

        return func(*args, **kwargs)
    return __wrapper


def auth_returned(func):

    @wraps(func)
    def __wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        try:
            obja = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM,])
        except Exception as e:
            abort(401)

        return func(*args, obj=obja, **kwargs)
    return __wrapper
