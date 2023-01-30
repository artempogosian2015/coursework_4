import pytest

from project.dao import UsersDAO
from project.dao.models.genres_model import Genre
from project.dao.models.users_model import User


@pytest.fixture
def users_dao(db):
    return UsersDAO(db.session)

@pytest.fixture
def user_1(db):
    u = User(email="a@b.com",
             password='12345',
             favorite_genre_id=1)
    g = Genre(name="Боевик")
    db.session.add(g)
    db.session.add(u)
    db.session.commit()
    return u

@pytest.fixture
def user_2(db):
    u = User(email="a2@botnet.com",
             password='qwerty',
             role='admin',
             favorite_genre_id=2)
    g = Genre(name="Комедия")
    db.session.add(g)
    db.session.add(u)
    db.session.commit()
    return u


class TestUsersDAO:

    def test_get_user_by_id(self, user_1, users_dao):
        assert users_dao.get_one(user_1.id) == user_1

    def test_get_user_by_id_not_found(self, users_dao):
        assert not users_dao.get_one(1)

    def test_get_all_users(self, users_dao, user_1, user_2):
        assert users_dao.get_all() == [user_1, user_2]

    def test_add_user(self, users_dao, user_to_add):
        users_dao.create(user_to_add)
        t_user = users_dao.get_one(1)
        assert t_user.name == user_to_add['name']
        assert t_user.password == user_to_add['password']

    def test_delete_user(self, users_dao, user_to_add):
        users_dao.create(user_to_add)
        t_user = users_dao.get_one(1)
        assert t_user.name == user_to_add['name']
        users_dao.delete(1)
        assert not users_dao.get_one(1)

    def test_get_by_email(self, users_dao, user_1):
        assert users_dao.get_by_email(user_1.email) == user_1

    def test_update(self, users_dao, user_2):
        assert users_dao.get_one(user_2.id) == user_2
        user_2.password = 'NEW ONE'
        users_dao.update(user_2)
        a = users_dao.get_one(user_2.id)
        assert a.password == 'NEW ONE'

    def test_get_users_by_page(self, app, users_dao, user_1, user_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert users_dao.get_all(page=1) == [user_1]
        assert users_dao.get_all(page=2) == [user_2]
        assert users_dao.get_all(page=3) == []
