from unittest.mock import patch

import pytest

from project.dao.models.favorites_model import Favorite
from project.dao.models.movies_model import Movie
from project.dao.models.users_model import User
from project.exceptions import ItemNotFound
from project.services import FavoritesService


class TestFavService:
    @pytest.fixture()
    @patch('project.dao.FavoritesDAO')
    def favorites_dao_mock(self, dao_mock, pass_hash):
        dao = dao_mock()
        dao.get_one.return_value = Favorite(user_id=1, movie_id=1)
        dao.get_movies.return_value = [
                                        Movie(id=1,
                                              title='test_movie',
                                              description='1234',
                                              trailer='link',
                                              year=1999,
                                              rating=7.0,
                                              genre_id=1,
                                              director_id=1
                                              ),

                                        Movie(id=2,
                                               title='test_movie2',
                                               description='1234',
                                               trailer='link',
                                               year=2009,
                                               rating=7.1,
                                               genre_id=1,
                                               director_id=1
                                              ),
        ]

        dao.get_users.return_value = [
            User(id=1, email='aaa@bbb.com', password=pass_hash[1]),
            User(id=2, email='test@user2.uk', password='qwertyhash'),
        ]

        dao.add_movie.return_value = Movie(
                                          id=1,
                                          title='test_movie',
                                          description='1234',
                                          trailer='link',
                                          year=1999,
                                          rating=7.0,
                                          genre_id=1,
                                          director_id=1
        )

        dao.delete_movie.return_value = None

        return dao

    @pytest.fixture()
    @patch('project.dao.MoviesDAO')
    def movies_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_one.return_value = Movie(id=1,
                                         title='test_movie',
                                         description='1234',
                                         trailer='link',
                                         year=1999,
                                         rating=7.0,
                                         genre_id=1,
                                         director_id=1
                                         )

    @pytest.fixture()
    def favorites_service(self, favorites_dao_mock):
        return FavoritesService(dao=favorites_dao_mock)

    @pytest.fixture
    def movie(self, db):
        obj = Movie(title="movie",
                    description='1234',
                    trailer='link',
                    year=1999,
                    rating=7.0,
                    genre_id=1,
                    director_id=1
                    )
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_get_one(self, favorites_service):
        f = favorites_service.get_one(1, 1)
        assert isinstance(f, Favorite)

    def test_get_movies(self, favorites_service):
        ml = favorites_service.get_movies(1)
        assert isinstance(ml[0], Movie)
        assert len(ml) == 2

    def test_get_users(self, favorites_service):
        ml = favorites_service.get_users(1)
        assert isinstance(ml[0], User)
        assert len(ml) == 2

    def test_create(self, favorites_service, movie):
        m = favorites_service.create(1, 1)
        assert isinstance(m, Movie)

    def test_create_out_of_bounds(self, favorites_service, movie):
        with pytest.raises(ItemNotFound):
            favorites_service.create(1, 3)

    def test_delete(self, favorites_service, favorites_dao_mock):
        favorites_service.delete(1, 1)
        assert favorites_dao_mock.delete_movie.called


