from typing import AsyncIterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from memes.periphery import loggers
from memes.periphery.db.sessions import postgres_session_factory
from memes.periphery.envs import Env
from memes.facade import adapters


class AdapterProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_connection(self) -> AsyncIterable[AsyncSession]:
        async with postgres_session_factory() as session:
            yield session

    @provide(scope=Scope.APP)
    async def get_media_gateway(self) -> adapters.gateways.MediaGateway:
        return adapters.gateways.MediaGateway(
            Env.media_host,
            Env.media_port,
            Env.media_ssl,
        )

    @provide(scope=Scope.REQUEST)
    async def get_memes(self, session: AsyncSession) -> adapters.repos.DBMemes:
        return adapters.repos.DBMemes(session, page_size=20)

    @provide(scope=Scope.APP)
    async def get_logger(self) -> adapters.loggers.Logger:
        return adapters.loggers.Logger(loggers.main_logger)

    @provide(scope=Scope.REQUEST)
    async def get_transaction(
        self,
        session: AsyncSession,
    ) -> adapters.transactions.DBTransaction:
        return adapters.transactions.DBTransaction(session)

