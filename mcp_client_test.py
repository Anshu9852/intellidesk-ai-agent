import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    params = StdioServerParameters(command=sys.executable, args=["mcp_server.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools mile:", [t.name for t in tools.tools])

            result = await session.call_tool("list_documents", {})
            print("list_documents ka result:", [c.text for c in result.content])


asyncio.run(main())