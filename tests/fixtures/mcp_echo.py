"""Local MCP transport fixture: no filesystem, network or external credentials."""
from mcp.server import MCPServer
import asyncio
import sys

server=MCPServer('Neutral test server')

@server.tool()
def add(a:int,b:int)->str:
    """Add two integers."""
    return str(a+b)

@server.tool()
async def wait_seconds(seconds:int)->str:
    """Wait to exercise cancellation."""
    await asyncio.sleep(seconds)
    return 'done'

if __name__=='__main__':
    if len(sys.argv)>1:server.run('streamable-http',host='127.0.0.1',port=int(sys.argv[1]))
    else:server.run()
