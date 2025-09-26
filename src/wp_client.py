from typing import Literal

import httpx

from src.utils.logger import get_logger

logger = get_logger(__name__)


class WPClient:
    def __init__(
        self,
        base_url: str,
        username: str,
        app_password: str,
    ):
        self.base_url = base_url
        self.username = username
        self.app_password = app_password
        self.api_root = f"{self.base_url.rstrip('/')}/wp-json/wp/v2"
        self._auth = httpx.BasicAuth(self.username, self.app_password)

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
        url = f'{self.api_root}/{endpoint}'

        try:
            async with httpx.AsyncClient(auth=self._auth, timeout=10.0) as client:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                return response
        except httpx.HTTPStatusError as e:
            logger.error(f'HTTP error occurred: {e.response.status_code} - {e.response.text}')
            raise
        except Exception as e:
            logger.error(f'Unexpected error occurred during request: {str(e)}')
            raise

    async def check_api_access(self) -> httpx.Response:
        """
        WordPress REST APIアクセス確認
        1件だけ投稿を取得して、APIアクセスが成功するか確認する

        Returns:
            httpx.Response: レスポンスオブジェクト
        """
        logger.info('Checking WordPress API access...')
        response = await self._request('GET', 'posts', params={'per_page': 1})
        return response

    async def fetch_posts(self, params: dict[str, any] | None = None) -> list[dict[str, any]]:
        """
        投稿一覧を取得する

        Args:
            params (dict, optional): クエリパラメータ。デフォルトはNone。

        Returns:
            list[dict]: 投稿データのリスト
        """
        logger.info('Fetching posts from WordPress...')
        response = await self._request('GET', 'posts', params=params or {})
        return response.json()

    async def get_post_by_id(self, post_id: int) -> dict[str, any]:
        """
        指定IDの投稿を取得する

        Args:
            post_id (int): 投稿ID

        Returns:
            dict: 投稿データ
        """
        logger.info(f'Fetching post with ID {post_id} from WordPress...')
        response = await self._request('GET', f'posts/{post_id}')
        logger.info(f'Post data: {response.json()}')
        return response.json()

    async def get_post_by_slug(self, slug: str) -> dict[str, any] | None:
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
