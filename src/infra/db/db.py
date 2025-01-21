from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.common.settings import get_settings


@dataclass(eq=False)
class AsyncPostgresClient:
    def __post_init__(self):
        self.engine = create_async_engine(get_settings().get_sql_url)
        self.session_factory = async_sessionmaker(bind=self.engine, class_=AsyncSession)

    @asynccontextmanager
    async def create_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            try:
                yield session
            finally:
                await session.close()
