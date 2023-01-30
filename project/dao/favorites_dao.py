from typing import List, Optional

import sqlalchemy.exc
from flask import current_app
from flask_restx import abort
from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc

from werkzeug.exceptions import NotFound

from project.dao.models.favorites_model import Favorite
from project.dao.models.movies_model import Movie
from project.dao.models.users_model import User


class FavoritesDAO:
    def __init__(self, session):
        self.session = session

    @property
    def _items_per_page(self) -> int:
        return current_app.config['ITEMS_PER_PAGE']

    def get_one(self, uid: int, mid: int):
        return self.session.query(Favorite).get((uid, mid))

    def get_movies(self, uid: int, page: Optional[int] = None, sort_by: Optional[str] = None) -> List[Favorite]:

        stmt: BaseQuery = self.session.query(Movie).join(Favorite).filter(Favorite.user_id == uid)
        if sort_by == 'created':
            stmt = stmt.order_by(desc(Favorite.created))
        elif sort_by == 'updated':
            stmt = stmt.order_by(desc(Favorite.updated))

        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()

    def get_users(self, mid: int, page: Optional[int] = None, sort_by: Optional[str] = None) -> List[Favorite]:

        stmt: BaseQuery = self.session.query(User).join(Favorite).filter(Favorite.movie_id == mid)
        if sort_by == 'created':
            stmt = stmt.order_by(desc(Favorite.created))
        elif sort_by == 'updated':
            stmt = stmt.order_by(desc(Favorite.updated))

        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()

    def add_movie(self, movie):
        self.session.add(movie)
        try:
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return None

        return movie

    def delete_movie(self, uid, mid):
        rec = self.get_one(uid, mid)
        if not rec:
            abort(404)
        self.session.delete(rec)
        self.session.commit()
