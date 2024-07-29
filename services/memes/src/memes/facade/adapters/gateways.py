import aiohttp

from memes.application.ports import gateways
from memes.domain import vos


class MediaGateway(gateways.media.Gateway):
    def __init__(self, media_host: str, media_port: int, ssl: bool) -> None:
        self.__media_host = media_host
        self.__media_port = media_port
        self.__ssl = ssl

    @property
    def __media_url(self) -> str:
        protocol = "https" if self.__ssl else "http"
        return f"{protocol}://{self.__media_host}:{self.__media_port}"

    def __media_image_endpoint_url_with(self, image_name: str) -> str:
        return f"{self.__media_url}/image/{image_name}"

    async def add_image(self, image: vos.Image) -> gateways.media.AdditionFailures | None:
        return await self.__put_image(image, for_first_time=True)

    async def update_image(self, image: vos.Image) -> gateways.media.AdditionFailures | None:
        return await self.__put_image(image, for_first_time=False)

    async def __put_image(
        self,
        image: vos.Image,
        for_first_time: bool,
    ) -> gateways.media.AdditionFailures | None:
        url = self.__media_image_endpoint_url_with(image.name)

        data = aiohttp.FormData()
        data.add_field("filename", image.name)
        data.add_field("file_content", image.content)

        async with aiohttp.ClientSession() as session:
            method = session.post if for_first_time else session.put
            async with method(url, data=data, ssl=self.__ssl) as response:
                if response.status == 400:
                    return gateways.media.AdditionFailures.unsupported_image_extension
                elif response.status != 200:
                    return gateways.media.AdditionFailures.media_is_not_working

    async def get_image_by_name(self, name: str) -> vos.Image| gateways.media.ReceivingFailures:
        url = self.__media_image_endpoint_url_with(name)

        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=self.__ssl) as response:
                if response.status == 404:
                    return gateways.media.ReceivingFailures.no_image
                elif response.status != 200:
                    return gateways.media.ReceivingFailures.media_is_not_working

                content = await response.read()
                return vos.Image(name=name, content=content)

    async def remove_by_name(self, name: str) -> gateways.media.RemovingFailures | None:
        url = self.__media_image_endpoint_url_with(name)

        async with aiohttp.ClientSession() as session:
            async with session.delete(url, ssl=self.__ssl) as response:
                if response.status != 200:
                    return gateways.media.RemovingFailures.media_is_not_working
