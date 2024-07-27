import asyncio

from media.model.services import setup


async def main() -> None:
    await setup.perform()


if __name__ == '__main__':
    asyncio.run(main())
