from src.infra.db.db import AsyncPostgresClient
from src.infra.models.base import Base


async def run_migrations():
    client: AsyncPostgresClient = AsyncPostgresClient()
    async with client.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
