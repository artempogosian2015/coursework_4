from .auth import api as auth_ns
from .users import api as users_ns

__all__ = [
    'auth_ns',
    'users_ns',
]
