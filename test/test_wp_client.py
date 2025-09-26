import pytest
from src.config.env_config import env_config
from src.wp_client import WPClient


@pytest.fixture
def wp_client():
    client = WPClient(
        base_url=env_config.WP_BASE_URL,
        username=env_config.WP_USER,
        app_password=env_config.WP_APP_PASSWORD,
    )
    return client


@pytest.fixture
def post_params():
    return {
        'per_page': 5,
        'orderby': 'date',
        'order': 'desc',
    }


@pytest.fixture
def post_info():
    return {
        'post_id': 1,
        'slug': 'hello-world',
    }


@pytest.mark.asyncio
async def test_check_api_access(wp_client):
    response = await wp_client.check_api_access()
    assert response is not None
    assert response.status_code == 200
    assert response.json() is not None


@pytest.mark.asyncio
async def test_fetch_posts(wp_client, post_params):
    response = await wp_client.fetch_posts(params=post_params)
    assert response is not None


@pytest.mark.asyncio
async def test_get_post_by_id(wp_client, post_info):
    post_id = post_info['post_id']
    post = await wp_client.get_post_by_id(post_id)
    assert post is not None
    assert post['id'] == post_id


@pytest.mark.asyncio
async def test_get_post_by_slug(wp_client, post_info):
    slug = post_info['slug']
    post = await wp_client.get_post_by_slug(slug)
    assert post is not None
    assert post['slug'] == slug
