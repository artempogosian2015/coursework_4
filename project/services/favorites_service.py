from typing import Optional, List

from project.config import config
from project.dao.daos import MoviesDAO, UsersDAO
from project.dao import FavoritesDAO
from project.dao.models.favorites_model import Favorite
from project.exceptions import ItemNotFound
from project.services import MoviesService, UsersService
from project.setup.db import db


class FavoritesService:
    def __init__(self, dao: FavoritesDAO) -> None:
        self.dao = dao
        mdao = MoviesDAO(db.session)
        self.ms = MoviesService(mdao)
        udao = UsersDAO(db.session)
        self.us = UsersService(udao)

    def get_one(self, uid: int, mid: int) -> Favorite:
        if fav := self.dao.get_one(uid, mid):
            return fav
        raise ItemNotFound(f'Movie {mid} is not favored by user {uid}.')

    def get_movies(self, uid: int, page: Optional[int] = None, sort_by: Optional[str] = None) -> List[Favorite]:
        return self.dao.get_movies(uid, page=page, sort_by=sort_by)

    def get_users(self, mid: int, page: Optional[int] = None, sort_by: Optional[str] = None) -> List[Favorite]:
        return self.dao.get_users(mid, page=page, sort_by=sort_by)

    def create(self, uid, mid):
        if self.ms.get_one(mid):
            movie = Favorite(user_id=uid, movie_id=mid)
            return self.dao.add_movie(movie)
        return None

    def delete(self, uid, mid):
        self.dao.delete_movie(uid, mid)


