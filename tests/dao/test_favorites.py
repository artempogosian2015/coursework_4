import pytest

from project.dao import FavoritesDAO
from project.dao.models.favorites_model import Favorite
from project.dao.models.users_model import User


@pytest.fixture
def favorites_dao(db):
    return FavoritesDAO(db.session)


@pytest.fixture
def user_1(db):
    u = User(email="a@b.com",
             password='12345',
             favorite_genre_id=1)
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture
def user_2(db):
    u = User(email="a2@botnet.com",
             password='qwerty',
             role='admin',
             favorite_genre_id=2)
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture
def fav_11(db, movie_1, user_1):
    f = Favorite(user_id=1,
                 movie_id=1)
    db.session.add(f)
    db.session.commit()
    return f


@pytest.fixture
def fav_21(db, movie_1, user_2):
    f = Favorite(user_id=2,
                 movie_id=1)
    db.session.add(f)
    db.session.commit()
    return f

@pytest.fixture
def movie_add_21():
    f = Favorite(user_id=2,
                 movie_id=1)
    return f


@pytest.fixture
def fav_12(db, movie_2, user_1):
    f = Favorite(user_id=1,
                 movie_id=2)
    db.session.add(f)
    db.session.commit()
    return f


@pytest.fixture
def fav_22(db, movie_2, user_2):
    f = Favorite(user_id=2,
                 movie_id=2)
    db.session.add(f)
    db.session.commit()
    return f


class TestFavoritesDAO:

    def test_get_favorite(self, fav_11, fav_21, fav_12, favorites_dao):
        assert favorites_dao.get_one(fav_11.user_id, fav_11.movie_id) == fav_11
        assert favorites_dao.get_one(fav_21.user_id, fav_21.movie_id) == fav_21
        assert favorites_dao.get_one(fav_12.user_id, fav_12.movie_id) == fav_12

    def test_favorite_not_found(self, favorites_dao):
        assert not favorites_dao.get_one(1, 1)

    def test_get_movies(self, favorites_dao, movie_1, movie_2, fav_11, fav_12):
        assert favorites_dao.get_movies(1) == [movie_1, movie_2]

    def test_get_movies_by_page(self, app, favorites_dao, movie_1, movie_2, fav_11, fav_12):
        app.config['ITEMS_PER_PAGE'] = 1
        assert favorites_dao.get_movies(1, page=1) == [movie_1]
        assert favorites_dao.get_movies(1, page=2) == [movie_2]
        assert favorites_dao.get_movies(1, page=3) == []

    def test_get_users(self, favorites_dao, user_1, user_2, fav_11, fav_21):
        assert favorites_dao.get_users(1) == [user_1, user_2]

    def test_get_users_by_page(self, app, favorites_dao, user_1, user_2, fav_11, fav_21):
        app.config['ITEMS_PER_PAGE'] = 1
        assert favorites_dao.get_users(1, page=1) == [user_1]
        assert favorites_dao.get_users(1, page=2) == [user_2]
        assert favorites_dao.get_users(1, page=3) == []

    def test_add_movie(self, favorites_dao, movie_1, user_2, movie_add_21):
        tst = favorites_dao.add_movie(movie_add_21)
        assert tst.user_id == 2
        assert tst.movie_id == 1

    def test_delete_movie(self, favorites_dao, movie_1, movie_2, fav_11, fav_12):
        assert favorites_dao.get_movies(1) == [movie_1, movie_2]
        favorites_dao.delete_movie(1, 1)
        assert favorites_dao.get_movies(1) == [movie_2]




