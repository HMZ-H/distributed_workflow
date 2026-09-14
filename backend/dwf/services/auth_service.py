from datetime import UTC, datetime, timedelta

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dwf.infrastructure.database.models import User
from dwf.settings import Settings


class AuthService:
    def __init__(self, db: AsyncSession, settings: Settings):
        self.db = db
        self.settings = settings
        self.password_hasher = PasswordHasher()

    async def register(self, email: str, password: str) -> User:
        existing = await self.db.execute(select(User).where(User.email == email))
        if existing.scalar_one_or_none() is not None:
            raise ValueError("Email already registered")

        hashed_password = self.password_hasher.hash(password)
        user = User(email=email, hashed_password=hashed_password)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def login(self, email: str, password: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user is None:
            return None
        try:
            self.password_hasher.verify(user.hashed_password, password)
            return user
        except VerifyMismatchError:
            return None

    def create_access_token(self, user_id: str) -> str:
        payload = {
            "sub": str(user_id),
            "type": "access",
            "exp": datetime.now(UTC) + timedelta(minutes=30),
        }
        return jwt.encode(payload, self.settings.jwt_secret_key, algorithm="HS256")

    def create_refresh_token(self, user_id: str) -> str:
        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": datetime.now(UTC) + timedelta(days=7),
        }
        return jwt.encode(payload, self.settings.jwt_secret_key, algorithm="HS256")

    def decode_token(self, token: str) -> dict:
        return jwt.decode(token, self.settings.jwt_secret_key, algorithms=["HS256"])
