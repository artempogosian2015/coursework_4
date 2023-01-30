from time import sleep

import pytest

from project.dao import DirectorsDAO
from project.dao.models.directors_model import Director


class TestDirectorsDAO:

    @pytest.fixture
    def directors_dao(self, db):
        return DirectorsDAO(db.session)

    @pytest.fixture
    def director_1(self, db):
        d = Director(name="Тест 1")
        db.session.add(d)
        db.session.commit()
        return d

    @pytest.fixture
    def director_2(self, db):
        d = Director(name="Тест 2")
        db.session.add(d)
        db.session.commit()
        return d

    @pytest.fixture
    def director_last(self, db):
        d = Director(name="Тест 3")
        sleep(1)
        db.session.add(d)
        db.session.commit()
        return d

    def test_get_director_by_id(self, director_1, directors_dao):
        assert directors_dao.get_one(director_1.id) == director_1

    def test_get_director_by_id_not_found(self, directors_dao):
        assert not directors_dao.get_one(1)

    def test_get_all_directors(self, directors_dao, director_1, director_2):
        assert directors_dao.get_all() == [director_1, director_2]

    def test_get_directors_by_page(self, app, directors_dao, director_1, director_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert directors_dao.get_all(page=1) == [director_1]
        assert directors_dao.get_all(page=2) == [director_2]
        assert directors_dao.get_all(page=3) == []

    def test_directors_by_created(self, directors_dao, director_1, director_2, director_last):
        assert directors_dao.get_all() == [director_1, director_2, director_last]
        assert directors_dao.get_all(sort_by='created') == [director_last, director_1, director_2]

    def test_directors_by_updated(self, directors_dao, director_1, director_2, director_last, db):
        dirs = directors_dao.get_all()
        assert dirs == [director_1, director_2, director_last]
        dirs[1].name = 'Тест 4'
        db.session.add(dirs[1])
        db.session.commit()
        assert directors_dao.get_all(sort_by='updated') == [director_2, director_last, director_1]
