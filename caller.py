import asyncio
from fastmcp import Client

client = Client("http://localhost:8002/mcp")

async def call_tool():
    async with client:
        result = await client.call_tool("get_file_at_commit", {"commit_hash": "22383e014ee8", "file_path": "/home/chirag/repo/devel/auction/events/api.py"})
        print(result)

asyncio.run(call_tool())