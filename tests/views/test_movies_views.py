import pytest

from project.dao.models.directors_model import Director
from project.dao.models.genres_model import Genre
from project.dao.models.movies_model import Movie


@pytest.fixture
def movie(db):
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


class TestMoviesView:


    @pytest.fixture
    def director(self, db):
        d = Director(name="Котик Крупноватый")
        db.session.add(d)
        db.session.commit()
        return d

    @pytest.fixture
    def genre(self, db):
        g = Genre(name="Комедия")
        db.session.add(g)
        db.session.commit()
        return g

    def test_many(self, client, movie, director, genre):
        response = client.get("/movies/")
        assert response.status_code == 200
        assert response.json == [{"id": movie.id, "title": movie.title,
                                  "description": movie.description,
                                  "trailer": movie.trailer,
                                  "year": movie.year,
                                  "rating": movie.rating,
                                  "genre_id": movie.genre_id,
                                  "director_id": movie.director_id,
                                  'director': director.name, # 'Котик Крупноватый',
                                  'genre': genre.name}]

    def test_movie_pages(self, client, movie):
        response = client.get("/movies/?page=1")
        assert response.status_code == 200
        assert len(response.json) == 1

        response = client.get("/movies/?page=2")
        assert response.status_code == 200
        assert len(response.json) == 0

    def test_movie(self, client, movie, director, genre):
        response = client.get("/movies/1/")
        assert response.status_code == 200
        assert response.json == {"id": movie.id, "title": movie.title,
                                  "description": movie.description,
                                  "trailer": movie.trailer,
                                  "year": movie.year,
                                  "rating": movie.rating,
                                  "genre_id": movie.genre_id,
                                  "director_id": movie.director_id,
                                  'director': director.name,
                                  'genre': genre.name}

    def test_movie_not_found(self, client, movie):
        response = client.get("/movies/2/")
        assert response.status_code == 404
