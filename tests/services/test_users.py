from unittest.mock import patch

import pytest

from project.config import config
from project.exceptions import ItemNotFound
from project.dao.models.users_model import User
from project.services import UsersService


class TestUsersService:

    @pytest.fixture()
    @patch('project.dao.UsersDAO')
    def users_dao_mock(self, dao_mock, pass_hash):
        dao = dao_mock()
        dao.get_one.return_value = User(id=1, email='aaa@bbb.com', password=pass_hash[1])
        dao.get_all.return_value = [
            User(id=1, email='aaa@bbb.com', password=pass_hash[1]),
            User(id=2, email='test@user2.uk', password='qwertyhash'),
            ]
        # return a password as a hash
        dao.get_by_email.return_value = User(id=1, email='aaa@bbb.com',
                                             password=pass_hash[1],)
                                            # b"FfPIRKseRPU0Ie9LWD+BopJfEf00xcwhbWnKHospGpE="
        dao.create.return_value = 'Ok'
        dao.update.return_value = 'Update ok'
        dao.delere.return_value = None

        return dao

    @pytest.fixture()
    def users_service(self, users_dao_mock):
        return UsersService(dao=users_dao_mock)

    @pytest.fixture
    def user(self, db, pass_hash):
        obj = User(email='aaa@bbb.com', password=pass_hash[1])
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_get_user(self, users_service, user):
        assert users_service.get_one(user.id)

    def test_user_not_found(self, users_dao_mock, users_service):
        users_dao_mock.get_one.return_value = None

        with pytest.raises(ItemNotFound):
            users_service.get_one(10)

    @pytest.mark.parametrize('page', [1, None], ids=['with page', 'without page'])
    def test_get_users(self, users_dao_mock, users_service, page):
        users = users_service.get_all(page=page, sort_by=None)
        assert len(users) == 2
        assert users == users_dao_mock.get_all.return_value
        users_dao_mock.get_all.assert_called_with(page=page, sort_by=None)

    @pytest.mark.parametrize('sort_by', ['created', None], ids=['with sort', 'without sort'])
    def test_get_users(self, users_dao_mock, users_service, sort_by):
        users = users_service.get_all(page=None, sort_by=sort_by)
        assert len(users) == 2
        assert users == users_dao_mock.get_all.return_value
        users_dao_mock.get_all.assert_called_with(page=None, sort_by=sort_by)

    def test_create(self, users_service, user_to_add):
        assert users_service.create(user_to_add) == 'Ok'

    def test_update(self, users_service, user, db):
        assert users_service.update(1, {'email': 'Testing'}) == 'Update ok'

    def test_change_password(self, users_service, user, passwords):
        assert users_service.change_password(1, passwords)

    def test_change_password_wrong(self, users_service, user, passwords):
        passwords['password_1'] = 'qwerty'
        assert not users_service.change_password(1, passwords)

    def test_make_hash(self, users_service, pass_hash):
        ha = users_service.make_password_hash(pass_hash[0])
        assert ha == pass_hash[1]

    def test_check_password(self, users_service, pass_hash):
        assert users_service.check_password(pass_hash[1], pass_hash[0], config.PWD_HASH_SALT, config.PWD_ALGO)

    def test_check_password_wrong(self, users_service, pass_hash):
        assert not users_service.check_password(pass_hash[1], 'qwerty', config.PWD_HASH_SALT, config.PWD_ALGO)


    def test_create_update_tokens(self, users_service, pass_hash):
        a = users_service.create_tokens('aaa@bbb.com', pass_hash[0])
        assert a is not None
        b = users_service.refresh_tokens(a['refresh_token'])
        assert b is not None

    def test_delete(self, users_service, users_dao_mock):
        users_service.delete(1)
        assert users_dao_mock.delete.called


