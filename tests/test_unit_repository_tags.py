import unittest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.orm import Session

from src.database.models import Tag, Photo

from src.repository.tags import get_tag_by_name, create_tag


class TestTagsRepository(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)

    def test_get_tag_by_name(self):
        tag = Tag()
        self.session.query().filter().first.return_value = tag
        result = get_tag_by_name(db=self.session, name='test')
        self.assertEqual(result, tag)

    def test_create_tag(self):
        tag = get_tag_by_name(self.session, name='test')
        result = create_tag(db=self.session, name='test')
        self.assertEqual(result, tag)
