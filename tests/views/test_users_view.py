import pytest
from unittest.mock import patch, MagicMock

from project.dao.models.genres_model import Genre
from project.dao.models.users_model import User
from project.services import UsersService
from project.container import user_service


class BaseTestUsers:
    @pytest.fixture
    def user(self, db, user_to_add):
        obj = User(email=user_to_add['email'],
                   password=b"FfPIRKseRPU0Ie9LWD+BopJfEf00xcwhbWnKHospGpE=",
                   favorite_genre_id=1,
                   name='John',
                   surname='Smith', )
        db.session.add(obj)
        db.session.commit()
        return obj

    @pytest.fixture
    def genre(self, db):
        g = Genre(name="Комедия")
        db.session.add(g)
        db.session.commit()
        return g


class TestUsersView(BaseTestUsers):
    def test_many(self, client, user, genre):
        response = client.get("/users/")
        assert response.status_code == 200
        assert 'password' not in response.json[0]
        assert response.json == [{"id": user.id, "email": user.email,
                                  "favorite_genre_id": user.favorite_genre_id,
                                  "name": user.name,
                                  "surname": user.surname,
                                  "role": user.role,
                                  "favorite_genre": genre.name}]

    def test_user_pages(self, client, user):
        response = client.get("/users/?page=1")
        assert response.status_code == 200
        assert len(response.json) == 1

        response = client.get("/users/?page=2")
        assert response.status_code == 200
        assert len(response.json) == 0

    def test_user(self, client, user, genre):
        mmock = MagicMock(return_value=True)
        with patch('jwt.decode', mmock):
            response = client.get("/users/1/", headers={'Authorization': 'Bearer mock'})

        assert response.status_code == 200, 'Not authorized'
        assert 'password' not in response.json
        assert response.json == {"id": user.id, "email": user.email,
                                 "favorite_genre_id": user.favorite_genre_id,
                                 "name": user.name,
                                 "surname": user.surname,
                                 "role": user.role,
                                 "favorite_genre": genre.name}

    def test_user_not_found(self, client, user):
        mmock = MagicMock(return_value=True)
        with patch('jwt.decode', mmock):
            response = client.get("/users/2/", headers={'Authorization': 'Bearer mock'})
        assert response.status_code == 404

    def test_user_auth(self, client, user):
        tokens = user_service.generate_jwt(user)
        response = client.get("/users/1/", headers={'Authorization': f'Bearer {tokens["access_token"]}'})
        assert response.status_code == 200
        response = client.get("/users/1/", headers={'Authorization': f'Bearer {tokens["refresh_token"][:-1]}'})
        assert response.status_code == 401

    def test_user_patch_not_auth(self, client, user, user_to_add):
        response = client.patch("/users/1/", json=user_to_add)
        assert response.status_code == 401

    def test_user_patch_auth(self, client, user, user_to_add):
        mmock = MagicMock(return_value=True)
        with patch('jwt.decode', mmock):
            response = client.patch("/users/1/", headers={'Authorization': 'Bearer mock'},
                                    json=user_to_add, follow_redirects=True)
        assert response.status_code == 204

    def test_user_put_not_auth(self, client, user, pass_hash, passwords):
        response = client.put("/users/1/", json=passwords)
        assert response.status_code == 401

    def test_user_put_wrong_pass(self, client, user, passwords):
        mmock = MagicMock(return_value=True)
        with patch('jwt.decode', mmock):
            pmock = MagicMock(return_value=None)
            with patch('project.container.user_service.change_password', pmock):
                response = client.put("/users/1/", headers={'Authorization': 'Bearer mock'},
                                      json=passwords)
        assert response.status_code == 401

    def test_user_put_correct_pass(self, client, user, passwords):
        mmock = MagicMock(return_value=True)
        with patch('jwt.decode', mmock):
            pmock = MagicMock(return_value=1)
            with patch('project.container.user_service.change_password', pmock):
                response = client.put("/users/1/", headers={'Authorization': 'Bearer mock'},
                                      json=passwords)
        assert response.status_code == 204
