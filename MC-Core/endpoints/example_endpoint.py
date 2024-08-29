from aiohttp import web


async def example_endpoint(request):
    return web.json_response({"message": "Hello, world!"})
