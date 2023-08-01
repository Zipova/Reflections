import unittest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.orm import Session

from src.database.models import Comment, User
from src.schemas import CommentModel

from src.repository.comments import add_comment, change_comment, delete_comment


class TestRateRepository(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_add_comment(self):
        body = CommentModel(comment='test')
        result = await add_comment(photo_id=1, body=body, current_user=self.user, db=self.session)
        self.assertEqual(result.comment, body.comment)
        self.assertTrue(hasattr(result, "user_id"))
        self.assertTrue(hasattr(result, "id"))

    async def test_change_comment_found(self):
        body = CommentModel(comment='test')
        comment = Comment()
        self.session.query().filter().first.return_value = comment
        self.session.commit.return_value = None
        result = await change_comment(photo_id=1, comment_id=1, body=body, current_user=self.user, db=self.session)
        self.assertEqual(result, comment)

    async def test_change_comment_not_found(self):
        body = CommentModel(comment='test')
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await change_comment(photo_id=1, comment_id=1, body=body, current_user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_delete_comment_found(self):
        comment = Comment()
        self.session.query().filter().first.return_value = comment
        result = await delete_comment(photo_id=1, comment_id=1, current_user=self.user, db=self.session)
        self.assertEqual(result, comment)

    async def test_delete_comment_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await delete_comment(photo_id=1, comment_id=1, current_user=self.user, db=self.session)
        self.assertIsNone(result)
