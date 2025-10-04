import asyncio
from contextlib import asynccontextmanager

import click
from fastmcp import FastMCP
from fastmcp.tools import Tool

from src.config.env_config import EnvConfig, env_config
from src.wordpress.tools.tool_manager import WordPressToolManager
from src.wordpress.wp_client import WordPressBasicClient, get_wordpress_client


class WordPressMCPServer:
    def __init__(
        self,
        base_url: str,
        username: str,
        app_password: str,
        host: str = 'localhost',
        port: int = 8080,
    ):
        self.base_url = base_url
        self.username = username
        self.app_password = app_password
        self.host = host
        self.port = port
        self._mcp = FastMCP(
            name='WordPress MCP Server',
            version='0.1.0',
            lifespan=self._config_lifecycle,
        )

    async def run_mcp(self):
        await self._mcp.run_async(
            transport='http',
            host=self.host,
            port=self.port,
        )

    @asynccontextmanager
    async def _config_lifecycle(self, server: FastMCP):
        async with get_wordpress_client(
            base_url=self.base_url,
            username=self.username,
            app_password=self.app_password,
        ) as wp_client:
            tool_manager = WordPressToolManager(client=wp_client)
            for name, tool in tool_manager.dict_tools.items():
                server.add_tool(Tool.from_function(fn=tool.coroutine, name=name, title=tool.name, description=tool.description))
            server.tool_manager = tool_manager

            yield
            server.tool_manager = None


@click.command()
@click.option('--host', default='localhost', help='サーバーホスト（デフォルト: localhost）')
@click.option('--port', default=8080, help='サーバーポート（デフォルト: 8080）')
@click.option('--url', default=env_config.WP_BASE_URL, help='WordPressサイトのベースURL（例: https://example.com）')
@click.option('--username', default=env_config.WP_USERNAME, help='WordPressのユーザー名')
@click.option('--app-password', default=env_config.WP_APP_PASSWORD, help='WordPressのアプリパスワード')
def start_server(host: str, port: int, url: str, username: str, app_password: str):
    server = WordPressMCPServer(
        base_url=url,
        username=username,
        app_password=app_password,
        host=host,
        port=port,
    )
    asyncio.run(server.run_mcp())
