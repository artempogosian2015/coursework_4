from typing import Optional, List

from project.dao import GenresDAO
from project.exceptions import ItemNotFound
from project.dao.models.genres_model import Genre


class GenresService:
    def __init__(self, dao: GenresDAO) -> None:
        self.dao = dao

    def get_one(self, pk: int) -> Genre:
        if genre := self.dao.get_one(pk):
            return genre
        raise ItemNotFound(f'Genre with pk={pk} does not exist.')

    def get_all(self, page: Optional[int] = None, sort_by: Optional[str] = None) -> List[Genre]:
        return self.dao.get_all(page=page, sort_by=sort_by)
