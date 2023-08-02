import unittest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.orm import Session

from src.database.models import Photo, User
from src.schemas import PhotoModel

from src.repository.photos import get_all_photos, get_user_photos, get_photo, remove_photo, update_description, \
    search_photo_by_keyword


class TestPhotosRepository(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_all_photos(self):
        photos = [Photo(), Photo(), Photo()]
        self.session.query().limit().offset().all.return_value = photos
        result = await get_all_photos(3, 0, self.session)
        self.assertEqual(result, photos)

    async def test_get_user_photos(self):
        photos = [Photo(), Photo(), Photo()]
        self.session.query().filter().limit().offset().all.return_value = photos
        result = await get_user_photos(limit=3, offset=0, user=self.user, db=self.session)
        self.assertEqual(result, photos)

    async def test_get_photo_found(self):
        photo = Photo()
        self.session.query().filter().first.return_value = photo
        result = await get_photo(photo_id=1, db=self.session)
        self.assertEqual(result, photo)

    async def test_get_photo_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_photo(photo_id=1, db=self.session)
        self.assertIsNone(result)

    async def test_remove_photo_found(self):
        photo = Photo()
        self.session.query().filter().first.return_value = photo
        result = await remove_photo(1, self.user, self.session)
        self.assertEqual(result, photo)

    async def test_remove_photo_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_photo(1, self.user, self.session)
        self.assertIsNone(result)

    async def test_update_description_found(self):
        body = PhotoModel(description='test', tags=['test', 'test'])
        photo = Photo()
        self.session.query().filter().first.return_value = photo
        self.session.commit.return_value = None
        result = await update_description(photo_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, photo)

    async def test_update_description_not_found(self):
        body = PhotoModel(description='test', tags=['test', 'test'])
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_description(photo_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_search_photo_by_keyword(self):
        photos = [Photo(), Photo(), Photo()]
        self.session.query().filter().all.return_value = photos
        result = await search_photo_by_keyword('test', 'test', self.session)
        self.assertEqual(result, photos)
