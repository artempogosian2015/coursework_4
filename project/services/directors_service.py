from typing import Optional, List

from project.dao import DirectorsDAO
from project.exceptions import ItemNotFound
from project.dao.models.directors_model import Director


class DirectorsService:
    def __init__(self, dao: DirectorsDAO) -> None:
        self.dao = dao

    def get_one(self, pk: int) -> Director:
        if director := self.dao.get_one(pk):
            return director
        raise ItemNotFound(f'Director with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None, sort_by: Optional[str] = None) -> List[Director]:
        return self.dao.get_all(page=page, sort_by=sort_by)
