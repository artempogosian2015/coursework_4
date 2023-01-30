from typing import Optional, List

from project.dao import MoviesDAO
from project.exceptions import ItemNotFound
from project.dao.models.movies_model import Movie


class MoviesService:
    def __init__(self, dao: MoviesDAO) -> None:
        self.dao = dao

    def get_one(self, pk: int) -> Movie:
        if movie := self.dao.get_one(pk):
            return movie
        raise ItemNotFound(f'Movie with pk={pk} does not exist.')

    def get_all(self, page: Optional[int] = None, status: Optional[str] = None, sort_by: Optional[str] = None) -> List[Movie]:
        if not status:
            return self.dao.get_all(page=page, sort_by=sort_by)
        return self.dao.get_sorted_by_year(page=page, status=status)
