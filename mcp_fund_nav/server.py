"""MCP server 入口: stdio 传输, 注册基金查询 tools。"""
import asyncio, json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from . import client

app = Server("mcp-fund-nav")

@app.list_tools()
async def list_tools():
    return [
        Tool(name="get_fund_estimate", description="查询单只基金实时估值",
             inputSchema={"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}),
        Tool(name="get_fund_history", description="查询基金最近 N 天历史净值",
             inputSchema={"type": "object", "properties": {"code": {"type": "string"}, "days": {"type": "integer", "default": 30}}, "required": ["code"]}),
        Tool(name="batch_estimate", description="批量查询多只基金估值",
             inputSchema={"type": "object", "properties": {"codes": {"type": "array", "items": {"type": "string"}}}, "required": ["codes"]}),
        Tool(name="search_fund", description="按名称或代码搜索基金",
             inputSchema={"type": "object", "properties": {"keyword": {"type": "string"}}, "required": ["keyword"]}),
    ]

@app.call_tool()
async def call_tool(name, arguments):
    if name == "get_fund_estimate":
        data = await client.fetch_estimate(arguments["code"])
    elif name == "get_fund_history":
        data = await client.fetch_history(arguments["code"], arguments.get("days", 30))
    elif name == "batch_estimate":
        data = [await client.fetch_estimate(c) for c in arguments["codes"]]
    elif name == "search_fund":
        data = await client.search(arguments["keyword"])
    else:
        raise ValueError(f"unknown tool {name}")
    return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False, indent=2))]

def main():
    async def _run():
        async with stdio_server() as (r, w):
            await app.run(r, w, app.create_initialization_options())
    asyncio.run(_run())

if __name__ == "__main__":
    main()
