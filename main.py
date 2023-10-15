import asyncio
from server import MyWebSocketHandler
from database import download_embeddings


async def main():
    await download_embeddings()
    handler = MyWebSocketHandler()
    await handler.start_server()

if __name__ == '__main__':
    asyncio.run(main())
