from unittest.mock import patch

import pytest

from project.exceptions import ItemNotFound
from project.dao.models.movies_model import Movie
from project.services import MoviesService


class TestMoviesService:

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
        dao.get_all.return_value = [
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
        dao.get_sorted_by_year.return_value = [Movie(id=1, title='Sorted movie 1',),
                                               Movie(id=2, title='Sorted movie 2',)]
        return dao

    @pytest.fixture()
    def movies_service(self, movies_dao_mock):
        return MoviesService(dao=movies_dao_mock)

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

    def test_get_movie(self, movies_service, movie):
        assert movies_service.get_one(movie.id)

    def test_movie_not_found(self, movies_dao_mock, movies_service):
        movies_dao_mock.get_one.return_value = None

        with pytest.raises(ItemNotFound):
            movies_service.get_one(10)

    @pytest.mark.parametrize('page', [1, None], ids=['with page', 'without page'])
    def test_get_movies_page(self, movies_dao_mock, movies_service, page):
        movies = movies_service.get_all(page=page, sort_by=None)
        assert len(movies) == 2
        assert movies == movies_dao_mock.get_all.return_value
        movies_dao_mock.get_all.assert_called_with(page=page, sort_by=None)

    @pytest.mark.parametrize('sort_by', ['created', None], ids=['with sort', 'without sort'])
    def test_get_movies_sort(self, movies_dao_mock, movies_service, sort_by):
        movies = movies_service.get_all(page=None, sort_by=sort_by)
        assert len(movies) == 2

    @pytest.mark.parametrize('status', ['new', None], ids=['with status', 'without status'])
    def test_get_movies_year(self, movies_dao_mock, movies_service, status):
        movies = movies_service.get_all(page=None, status=status)
        assert len(movies) == 2

