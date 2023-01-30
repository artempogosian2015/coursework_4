import pytest
from unittest.mock import patch, MagicMock

from project.container import user_service
from project.dao.models.users_model import User
from tests.views.test_movies_views import movie
from tests.dao.test_favorites import fav_11, fav_12, fav_21, user_1, user_2, movie_1, movie_2



@pytest.fixture
def fav_obj():
    return {
                'id': 1,
                'email': 'user_obj.email',
                'role': 'user',
            }

@pytest.fixture
def user(db, user_to_add):
    obj = User(email=user_to_add['email'],
               password=b"FfPIRKseRPU0Ie9LWD+BopJfEf00xcwhbWnKHospGpE=",
               favorite_genre_id=1,
               name='John',
               surname='Smith', )
    db.session.add(obj)
    db.session.commit()
    return obj


class TestFavsView:

    def test_movie_add(self, client, fav_obj, movie):
        mmock = MagicMock(return_value=fav_obj)
        with patch('jwt.decode', mmock):
            response = client.post("/favorites/movies/1", headers={'Authorization': 'Bearer mock'})
        assert response.status_code == 201

    def test_movie_add_non_existent(self, client, fav_obj, movie):
        mmock = MagicMock(return_value=fav_obj)
        with patch('jwt.decode', mmock):
            response = client.post("/favorites/movies/2", headers={'Authorization': 'Bearer mock'})
        assert response.status_code == 404

    def test_movie_add_duplicate(self, client, fav_obj, movie):
        mmock = MagicMock(return_value=fav_obj)
        with patch('jwt.decode', mmock):
            client.post("/favorites/movies/1", headers={'Authorization': 'Bearer mock'})
            response = client.post("/favorites/movies/1", headers={'Authorization': 'Bearer mock'})
        assert response.status_code == 409

    def test_movie_add_auth(self, client, user, movie):
        tokens = user_service.generate_jwt(user)
        response = client.post("/favorites/movies/1", headers={'Authorization': f'Bearer {tokens["access_token"]}'})
        assert response.status_code == 201

    def test_movie_add_auth_fail(self, client, user, movie):
        response = client.post("/favorites/movies/1", headers={'Authorization': f'Bearer dhjaklehwuiladlabd'})
        assert response.status_code == 401

    def test_movie_delete(self, client, movie, fav_11, fav_obj):
        mmock = MagicMock(return_value=fav_obj)
        with patch('jwt.decode', mmock):
            response = client.delete("/favorites/movies/1", headers={'Authorization': 'Bearer mock'})
        assert response.status_code == 204

    def test_movie_delete_auth(self, client, movie, fav_11, user):
        tokens = user_service.generate_jwt(user)
        response = client.post("/favorites/movies/1", headers={'Authorization': f'Bearer {tokens["access_token"]}'})
        assert response.status_code == 201
        response = client.delete("/favorites/movies/1", headers={'Authorization': f'Bearer {tokens["access_token"]}'})
        assert response.status_code == 204

    def test_movies_list(self, client, fav_11, fav_12):
        response = client.get("/favorites/users/1")
        assert response.status_code == 200
        assert len(response.json) == 2
        response = client.get("/favorites/users/2")
        assert response.json == []

    def test_users_list(self, client, fav_11, fav_21):
        response = client.get("/favorites/movies/1")
        assert response.status_code == 200
        assert len(response.json) == 2
        response = client.get("/favorites/movies/2")
        assert response.json == []

