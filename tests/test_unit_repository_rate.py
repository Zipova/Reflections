import unittest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.orm import Session

from src.database.models import Rate, Photo, User
from src.schemas import RateModel

from src.repository.rate import update_avg_photo_rating, get_rating_by_id, remove_rating, get_rating


class TestRateRepository(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.photo = Photo(id=1, rated_by=[])

    async def test_update_avg_photo_rating(self):
        photo = Photo()
        result = await update_avg_photo_rating(photo, self.session)
        self.assertEqual(result, photo)

    async def test_get_rating_by_id_found(self):
        rating = Rate()
        self.session.query(Rate).filter_by().first.return_value = rating
        result = await get_rating_by_id(1, self.session)
        self.assertEqual(result, rating)

    async def test_get_rating_by_id_not_found(self):
        self.session.query(Rate).filter_by().first.return_value = None
        result = await get_rating_by_id(1, self.session)
        self.assertIsNone(result)

    async def test_remove_rating_found(self):
        rating = Rate()
        self.session.query(Rate).filter_by().first.return_value = rating
        result = await remove_rating(1, self.session)
        self.assertEqual(result, rating)

    async def test_remove_rating_not_found(self):
        self.session.query(Rate).filter_by().first.return_value = None
        result = await remove_rating(1, self.session)
        self.assertIsNone(result)

    async def test_get_rating(self):
        ratings = [Rate(), Rate(), Rate()]
        self.session.query(Rate).limit().offset().all.return_value = ratings
        result = await get_rating(10, 0, self.session)
        self.assertEqual(result, ratings)
