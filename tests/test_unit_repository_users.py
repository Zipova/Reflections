import unittest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.schemas import UserModel

from src.repository.users import get_user_by_email, create_user, update_token, confirmed_email, update_avatar


class TestUsersRepository(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)

    async def test_get_user_by_email_found(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email='test@test.ua', db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email='test@test.ua', db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        body = UserModel(
            username='testtest',
            email='test@test.ua',
            password='test123'
        )
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)

    async def test_update_token(self):
        user = User()
        user.refresh_token = None
        refresh_token = 'test_token'
        await update_token(user=user, token=refresh_token, db=self.session)
        self.assertEqual(user.refresh_token, refresh_token)

    async def test_confirmed_email(self):
        user = User(email='test@test.ua', confirmed=False)
        self.session.add(user)
        self.session.commit()
        user_id = user.id
        await confirmed_email(email=user.email, db=self.session)
        result = self.session.query(User).get(user_id)
        self.assertTrue(result.confirmed)

    async def test_update_avatar(self):
        user = User()
        user.avatar = 'avatar'
        avatar_url = 'avatar_url'
        result = await update_avatar(email=user.email, url=avatar_url, db=self.session)
        self.assertEqual(avatar_url, result.avatar)

    async def test_block_token(self):
        token = "token"
        user = User(id=1, refresh_token=token)
        repository_users.auth.auth_service.verify_access_token = MagicMock()
        # repository_users.auth.auth_service.get_exp_by_access_token = MagicMock(return_value=1)
        repository_users.client_redis = AsyncMock()
        auth_service.redis_cache = AsyncMock()
        self.session.query().filter().first.return_value = user
        result = await repository_users.block_token(token=token, db=self.session)
        self.assertIsNone(user.refresh_token)
        self.assertIsNone(result)
