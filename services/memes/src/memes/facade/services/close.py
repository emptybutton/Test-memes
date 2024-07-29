from memes.facade.di.containers import adapter_container


async def perform() -> None:
    await adapter_container.close()
