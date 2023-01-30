import base64
import calendar
import datetime
import hashlib
import hmac
from typing import Optional, List

import jwt
from flask_restx import abort

from project.dao import UsersDAO
from project.exceptions import ItemNotFound
from project.dao.models.users_model import User
from project.config import config


class UsersService:
    def __init__(self, dao: UsersDAO) -> None:
        self.dao = dao

    def get_one(self, pk: int) -> User:
        if user := self.dao.get_one(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} does not exist.')

    def create_tokens(self, email, password):
        user = self.dao.get_by_email(email)

        if user is None:
            return None

        if self.check_password(user.password, password, config.PWD_HASH_SALT, config.PWD_ALGO):
            return self.generate_jwt(user)

        return None

    def refresh_tokens(self, refresh_token):

        try:
            data = jwt.decode(jwt=refresh_token, key=config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM, ])
        except Exception as e:
            return None

        email = data.get('email')

        user = self.dao.get_by_email(email)

        return self.generate_jwt(user)

    def get_all(self, page: Optional[int] = None, sort_by: Optional[str] = None) -> List[User]:
        return self.dao.get_all(page=page, sort_by=sort_by)

    def create(self, user_d):
        user_d['password'] = self.make_password_hash(user_d.get('password'))
        return self.dao.create(user_d)

    def update(self, uid, user_d):
        user = self.get_one(uid)

        if 'email' in user_d:
            user.email = user_d.get('email')
        if 'name' in user_d:
            user.name = user_d.get('name')
        if 'surname' in user_d:
            user.surname = user_d.get('surname')
        if 'favorite_genre_id' in user_d:
            user.favorite_genre_id = user_d.get('favorite_genre_id')

        return self.dao.update(user)

    def change_password(self, uid, passwords):
        user = self.get_one(uid)
        if self.check_password(user.password, passwords["password_1"], config.PWD_HASH_SALT, config.PWD_ALGO):
            user.password = self.make_password_hash(passwords["password_2"])
            self.dao.update(user)
            return 1
        return None

    def delete(self, rid):
        self.dao.delete(rid)

    def make_password_hash(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            config.PWD_ALGO,
            password.encode('utf-8'),
            config.PWD_HASH_SALT,
            config.PWD_HASH_ITERATIONS
        ))

    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            config.PWD_ALGO,
            password.encode('utf-8'),  # Convert the password to bytes
            config.PWD_HASH_SALT,
            config.PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

    def generate_jwt(self, user_obj):
        data = {
            'id': user_obj.id,
            'email': user_obj.email,
            'role': user_obj.role,
        }
        mins30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(mins30.timetuple())
        access_token = jwt.encode(data, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
        return {'access_token': access_token, 'refresh_token': refresh_token}

    def check_password(self, password_hash, incoming_password, salt, algo):
        return hmac.compare_digest(
            base64.b64decode(password_hash),
            hashlib.pbkdf2_hmac(algo, incoming_password.encode('utf-8'), salt, config.PWD_HASH_ITERATIONS)
        )

