from typing import Optional, List

from flask_restx import abort
from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO, T
from project.dao.models.genres_model import Genre
from project.dao.models.directors_model import Director
from project.dao.models.movies_model import Movie
from project.dao.models.users_model import User


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_sorted_by_year(self, page: Optional[int] = None, status: Optional[str] = None) -> List[T]:
        stmt: BaseQuery = self._db_session.query(self.__model__)
        if status == 'new':
            stmt = stmt.order_by(desc(self.__model__.year))

        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()


class UsersDAO(BaseDAO[User]):
    __model__ = User

    def create(self, user_d):
        ent = User(**user_d)
        self._db_session.add(ent)
        self._db_session.commit()
        return ent

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).first()

    def delete(self, rid):
        user = self.get_one(rid)
        if not user:
            abort(404)
        self._db_session.delete(user)
        self._db_session.commit()

    def update(self, user):
        self._db_session.add(user)
        self._db_session.commit()
