import logging
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastmcp.client import Client as MCPClient
from src.config.env_config import env_config
from src.utils.logger import get_logger
from src.wordpress.mcp.server import WordPressMCPServer
from src.wordpress.schemas import FetchPostsResult, PostSchema, WPPreviousPost

logger = get_logger(__name__)
logger.setLevel(logging.DEBUG)


@pytest.fixture
def wp_mcp_server() -> WordPressMCPServer:
    return WordPressMCPServer(
        base_url=env_config.WP_BASE_URL,
        username=env_config.WP_USERNAME,
        app_password=env_config.WP_APP_PASSWORD,
        transport='stdio',
    )


@pytest_asyncio.fixture
async def wp_mcp_client(wp_mcp_server: WordPressMCPServer) -> AsyncGenerator[MCPClient, None]:
    async with MCPClient(wp_mcp_server.mcp) as client:
        yield client


class TestWordPressMCPServer:
    @pytest.fixture
    def post_data(self):
        return {
            'title': 'Test Post from MCP',
            'content': 'This is a test post created via the MCP tool.',
            'status': 'draft',
        }

    @pytest.mark.asyncio
    async def test_connect_mcp(self, wp_mcp_client: MCPClient):
        assert await wp_mcp_client.ping() is True

    @pytest.mark.asyncio
    async def test_get_tools(self, wp_mcp_client: MCPClient, wp_mcp_server: WordPressMCPServer):
        tools = await wp_mcp_client.list_tools()
        logger.debug('Available Tools: %s', tools)
        assert len(tools) > 0
        assert len(tools) == len(wp_mcp_server.tool_manager.dict_tools.values())
        for tool in tools:
            assert tool.name in wp_mcp_server.tool_manager.dict_tools.keys()
            assert tool.description is not None
            assert tool.inputSchema is not None

    @pytest.mark.asyncio
    async def test_fetch_posts_tool(self, wp_mcp_client: MCPClient):
        result = await wp_mcp_client.call_tool('fetch_posts_tool', {'params': {'per_page': 1}})
        result_content = result.structured_content
        posts_result = FetchPostsResult.model_validate(result_content)
        assert isinstance(posts_result, FetchPostsResult)
        assert isinstance(posts_result.posts, list)
        assert len(posts_result.posts) != 0

    @pytest.mark.asyncio
    async def test_get_post_by_id_tool(self, wp_mcp_client: MCPClient):
        tool_response = await wp_mcp_client.call_tool('get_post_by_id_tool', {'post_id': 1})

        post_result = PostSchema.model_validate(tool_response.structured_content)
        logger.debug('PostSchema by ID: %s', post_result)
        assert isinstance(post_result, PostSchema)
        assert post_result.id == 1

    @pytest.mark.asyncio
    async def test_get_post_by_slug_tool(self, wp_mcp_client: MCPClient):
        tool_response = await wp_mcp_client.call_tool('get_post_by_slug_tool', {'slug': 'hello-world'})

        post_result = PostSchema.model_validate(tool_response.structured_content)
        logger.debug('PostSchema by Slug: %s', post_result)
        assert isinstance(post_result, PostSchema)
        assert post_result.slug == 'hello-world'

    @pytest.mark.asyncio
    async def test_create_and_delete_post_tool(self, wp_mcp_client: MCPClient, post_data):
        post_tool_response = await wp_mcp_client.call_tool('create_post_tool', post_data)

        post_result = PostSchema.model_validate(post_tool_response.structured_content)
        logger.debug('Created PostSchema: %s', post_result)
        assert isinstance(post_result, PostSchema)

        delete_tool_response = await wp_mcp_client.call_tool('delete_post_tool', {'post_id': post_result.id, 'force': True})
        delete_result = WPPreviousPost.model_validate(delete_tool_response.structured_content)
        logger.debug('Deleted PostSchema: %s', delete_result)
        assert isinstance(delete_result, WPPreviousPost)
        assert delete_result.id == post_result.id
