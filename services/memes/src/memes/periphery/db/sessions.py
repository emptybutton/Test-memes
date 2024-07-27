from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from memes.periphery.db import engines


postgres_session_factory = sessionmaker(
    engines.postgres_engine,
    class_=AsyncSession,
)
