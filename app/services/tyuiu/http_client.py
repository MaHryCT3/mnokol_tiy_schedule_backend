import aiohttp
from loguru import logger


class HTTPClient:
    def __init__(self, session: aiohttp.ClientSession = None):
        self._session = session or aiohttp.ClientSession()

    async def request_raw(
        self, url: str, http_method: str = 'GET', params: dict | None = None, data: dict | None = None
    ) -> aiohttp.ClientResponse:
        async with self._session.request(http_method, url, params=params, data=data) as response:
            await response.read()
        logger.debug('Get response from {} {} ->\n{}', http_method, response.url, await response.text())
        return response

    async def request_json(
        self, url: str, http_method: str = 'GET', params: dict | None = None, data: dict | None = None
    ) -> dict:
        response = await self.request_raw(url, http_method, params=params, data=data)
        return await response.json(content_type=None)

    async def request_text(
        self, url: str, http_method: str = 'GET', params: dict | None = None, data: dict | None = None
    ) -> str:
        response = await self.request_raw(url, http_method, params=params, data=data)
        return await response.text()
