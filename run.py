from project.config import config
from project.dao.models.genres_model import Genre
from project.dao.models.directors_model import Director
from project.dao.models.movies_model import Movie
from project.dao.models.users_model import User
from project.server import create_app, db

app = create_app(config)


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "Director": Director,
        "Movie": Movie,
        "User": User
    }


if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)