from .auth import auth_ns, users_ns
from .main import genres_ns, movies_ns, directors_ns, favorites_ns

__all__ = [
    'auth_ns',
    'genres_ns',
    'users_ns',
    'movies_ns',
    'directors_ns',
    'favorites_ns'
]
