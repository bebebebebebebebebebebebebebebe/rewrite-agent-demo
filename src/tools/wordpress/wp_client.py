from typing import Literal

import httpx

from src.config.env_config import env_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class WordPressBasicClient:
    def __init__(
        self,
        base_url: str,
        username: str,
        app_password: str,
        time_out: float = 10.0,
    ):
        self.base_url = base_url
        self.username = username
        self.app_password = app_password
        self.api_root = f'{self.base_url.rstrip("/")}/wp-json/wp/v2'
        self._auth = httpx.BasicAuth(self.username, self.app_password)
        self._time_out = time_out
        self._client: httpx.AsyncClient | None = None

    async def init_client(self):
        if self._client is None:
            self._client = httpx.AsyncClient(auth=self._auth, timeout=self._time_out)
            logger.info('Initialized httpx.AsyncClient for WordPressBasicClient.')

    async def close_client(self):
        if self._client is not None:
            await self._client.aclose()
            self._client = None
            logger.info('Closed httpx.AsyncClient for WordPressBasicClient.')

    async def _request(self, method: Literal['GET', 'POST', 'PUT', 'DELETE'], endpoint: str, **kwargs) -> httpx.Response:
        """
        共通リクエスト処理、エラーハンドリング

        Args:
            method (str): HTTPメソッド
            endpoint (str): APIエンドポイント
            **kwargs: httpxのリクエストに渡す追加パラメータ

        Returns:
            httpx.Response: レスポンスオブジェクト
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")
        url = f'{self.api_root}/{endpoint}'
        logger.debug('WP %s %s params=%s json=%s', method, url, kwargs.get('params'), kwargs.get('json'))

        try:
            response = await self._client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            logger.error(f'HTTP error occurred: {e.response.status_code} - {e.response.text}')
            raise
        except Exception as e:
            logger.error(f'Unexpected error occurred during request: {str(e)}')
            raise

    async def wp_check_api_access(self) -> httpx.Response:
        """
        WordPress REST APIアクセス確認
        1件だけ投稿を取得して、APIアクセスが成功するか確認する

        Returns:
            httpx.Response: レスポンスオブジェクト
        """
        logger.info('Checking WordPress API access...')
        response = await self._request('GET', 'posts', params={'per_page': 1})
        return response

    async def wp_fetch_items_by_ids(
        self, item_type: Literal['posts', 'users', 'categories', 'tags'], ids: list[int]
    ) -> list[dict[str, any]]:
        """
        指定されたIDのアイテムを一括取得する

        Args:
            item_type (Literal["posts", "users", "categories", "tags"]): 取得するアイテムのタイプ
            ids (list[int]): 取得したいアイテムのIDリスト

        Returns:
            list[dict]: アイテムデータのリスト
        """
        if not ids:
            return []

        logger.info(f'Fetching {item_type} with IDs {ids} from WordPress...')
        params = {'include': ','.join(map(str, ids))}
        response = await self._request('GET', item_type, params=params)
        return response.json()

    async def wp_fetch_posts(self, params: dict[str, any] | None = None) -> list[dict[str, any]]:
        """
        投稿一覧を取得する

        Args:
            params (dict, optional): クエリパラメータ。デフォルトはNone。

        Returns:
            list[dict]: 投稿データのリスト
        """
        logger.info(f'Fetching posts from WordPress: url={self.api_root}/posts, params={params}')
        response = await self._request('GET', 'posts', params=params if params else {})
        return response.json()

    async def wp_get_user_by_id(self, user_id: int) -> dict[str, any]:
        """
        指定IDのユーザーを取得する

        Args:
            user_id (int): ユーザーID

        Returns:
            dict: ユーザーデータ
        """
        logger.info(f'Fetching user with ID {user_id} from WordPress...')
        response = await self._request('GET', f'users/{user_id}')
        logger.info(f'User data: {response.json()}')
        return response.json()

    async def wp_get_post_by_id(self, post_id: int) -> dict[str, any]:
        """
        指定IDの投稿を取得する

        Args:
            post_id (int): 投稿ID

        Returns:
            dict: 投稿データ
        """
        logger.info(f'Fetching post with ID {post_id} from WordPress...')
        response = await self._request('GET', f'posts/{post_id}')

        if response.status_code == 404:
            logger.warning(f'Post with ID {post_id} not found.')
            return {}
        logger.info(f'Post data: {response.json()}')
        return response.json()

    async def wp_get_post_by_slug(self, slug: str) -> dict[str, any] | None:
        """
        指定スラッグの投稿を取得する

        Args:
            slug (str): 投稿スラッグ

        Returns:
            dict | None: 投稿データ、存在しない場合はNone
        """
        logger.info(f"Fetching post with slug '{slug}' from WordPress...")
        response = await self._request('GET', 'posts', params={'slug': slug})
        posts = response.json()
        return posts[0] if posts else None

    async def wp_create_post(self, title: str, content: str, status: str = 'draft') -> dict[str, any]:
        """
        新しい投稿を作成する

        Args:
            title (str): 投稿タイトル
            content (str): 投稿内容
            status (str, optional): 投稿ステータス。デフォルトは"draft"。

        Returns:
            dict: 作成された投稿データ
        """
        logger.info(f"Creating a new post with title '{title}'...")
        data = {
            'title': title,
            'content': content,
            'status': status,
        }
        response = await self._request('POST', 'posts', json=data)
        logger.info(f'Created post data: {response.json()}')
        return response.json()


def get_wp_client(
    base_url: str = env_config.WP_BASE_URL,
    username: str = env_config.WP_USER,
    app_password: str = env_config.WP_APP_PASSWORD,
) -> WordPressBasicClient:
    return WordPressBasicClient(
        base_url=base_url,
        username=username,
        app_password=app_password,
    )
