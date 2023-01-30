import pytest

from project.dao import MoviesDAO
from project.dao.models.directors_model import Director
from project.dao.models.genres_model import Genre
from project.dao.models.movies_model import Movie


@pytest.fixture
def movies_dao(db):
    return MoviesDAO(db.session)


@pytest.fixture
def movie_1(db):
    m = Movie(title="Фильм 1",
              description="Текст 5",
              trailer="https://www.youtube.com/watch?v=BB61nauFkds",
              year=1902,
              rating=3.4,
              genre_id=1,
              director_id=1, )
    d = Director(name="Зайчик Крошечный")
    g = Genre(name="Боевик")
    db.session.add(g)
    db.session.add(d)
    db.session.add(m)
    db.session.commit()
    return m


@pytest.fixture
def movie_2(db):
    m = Movie(title="Фильм 2",
              description="Тест 68",
              trailer="https://www.youtube.com/watch?v=BB61nauFkds",
              year=2025,
              rating=9.4,
              genre_id=2,
              director_id=2, )
    d = Director(name="Тест 7")
    g = Genre(name="Комедия")
    db.session.add(g)
    db.session.add(d)
    db.session.add(m)
    db.session.commit()
    return m


class TestMoviesDAO:

    def test_get_movie_by_id(self, movie_1, movies_dao):
        assert movies_dao.get_one(movie_1.id) == movie_1

    def test_get_movie_by_id_not_found(self, movies_dao):
        assert not movies_dao.get_one(1)

    def test_get_all_movies(self, movies_dao, movie_1, movie_2):
        assert movies_dao.get_all() == [movie_1, movie_2]

    def test_get_movies_by_page(self, app, movies_dao, movie_1, movie_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert movies_dao.get_all(page=1) == [movie_1]
        assert movies_dao.get_all(page=2) == [movie_2]
        assert movies_dao.get_all(page=3) == []

    def test_get_movies_by_year(self, movies_dao, movie_1, movie_2):
        assert movies_dao.get_sorted_by_year(status=None) == [movie_1, movie_2]
        assert movies_dao.get_sorted_by_year(status='new') == [movie_2, movie_1]
