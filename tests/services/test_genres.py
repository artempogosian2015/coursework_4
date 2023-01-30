from unittest.mock import patch

import pytest

from project.exceptions import ItemNotFound
from project.dao.models.genres_model import Genre
from project.services import GenresService


class TestGenresService:

    @pytest.fixture()
    @patch('project.dao.GenresDAO')
    def genres_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_one.return_value = Genre(id=1, name='test_genre')
        dao.get_all.return_value = [
            Genre(id=1, name='test_genre_1'),
            Genre(id=2, name='test_genre_2'),
        ]
        return dao

    @pytest.fixture()
    def genres_service(self, genres_dao_mock):
        return GenresService(dao=genres_dao_mock)

    @pytest.fixture
    def genre(self, db):
        obj = Genre(name="genre")
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_get_genre(self, genres_service, genre):
        assert genres_service.get_one(genre.id)

    def test_genre_not_found(self, genres_dao_mock, genres_service):
        genres_dao_mock.get_one.return_value = None

        with pytest.raises(ItemNotFound):
            genres_service.get_one(10)

    @pytest.mark.parametrize('page', [1, None], ids=['with page', 'without page'])
    def test_get_genres(self, genres_dao_mock, genres_service, page):
        genres = genres_service.get_all(page=page, sort_by=None)
        assert len(genres) == 2
        assert genres == genres_dao_mock.get_all.return_value
        genres_dao_mock.get_all.assert_called_with(page=page, sort_by=None)

    @pytest.mark.parametrize('sort_by', ['created', None], ids=['with sort', 'without sort'])
    def test_get_genres(self, genres_dao_mock, genres_service, sort_by):
        genres = genres_service.get_all(page=None, sort_by=sort_by)
        assert len(genres) == 2
        assert genres == genres_dao_mock.get_all.return_value
        genres_dao_mock.get_all.assert_called_with(page=None, sort_by=sort_by)
