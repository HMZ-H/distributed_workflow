import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from dwf.infrastructure.database.models import Base
from dwf.main import create_app
from dwf.api.deps import get_db
from dwf.settings import Settings

TEST_DATABASE_URL = "sqlite+aiosqlite:///test.db"


@pytest.fixture()
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture()
async def db_session(engine):
    session_factory = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_factory() as session:
        yield session


@pytest.fixture()
async def client(db_session):
    settings = Settings(
        app_name="test",
        database_url=TEST_DATABASE_URL,
        jwt_secret_key="test-secret-key",
        log_level="info",
    )
    app = create_app(settings)

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
