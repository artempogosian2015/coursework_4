from project.container import user_service
from tests.views.test_users_view import BaseTestUsers


class TestAuthView(BaseTestUsers):

    def test_register(self, client, user_to_add):
        response = client.post('/auth/register', json=user_to_add)
        assert response.status_code == 201

    def test_register_fail(self, client, user_to_add):
        response = client.post('/auth/register', json={'email': 'a@mama.com'})
        assert response.status_code == 400

    def test_login(self, client, user, user_to_add):
        response = client.post('/auth/login', json=user_to_add)
        assert response.status_code == 200

    def test_login_fail(self, client, user, user_to_add):
        response = client.post('/auth/login', json={'email': 'a@baba.ku',
                                                    'password': user_to_add['password']})
        assert response.status_code == 401
        response = client.post('/auth/login', json={'email': user_to_add['email'],
                                                    'password': 'qwerty'})
        assert response.status_code == 401

    def test_update_token(self, client, user):
        tokens = user_service.generate_jwt(user)
        response = client.put("/auth/login", json=tokens)
        assert response.status_code == 200

    def test_update_fail(self, client, user):
        response = client.put("/auth/login", json={'password': 'qwerty'})
        assert response.status_code == 400
        response = client.put("/auth/login", json={"refresh_token": 'ewqheuihwndkjsa'})
        assert response.status_code == 400
