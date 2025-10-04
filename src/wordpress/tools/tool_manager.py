import asyncio
from datetime import datetime
from typing import Dict, List, Literal

import html2text
from langchain_core.tools import StructuredTool

from src.wordpress.schemas import FetchPostsResult, PostListQueryParams, PostSchema
from src.wordpress.wp_client import WordPressBasicClient


class WordPressToolManager:
    def __init__(
        self,
        client: WordPressBasicClient,
    ):
        """
        WordPressの投稿管理ツールマネージャー

        Args:
            client (WordPressBasicClient): 認証されたWordPressクライアントインスタンス
        """
        self.client = client

    @property
    def dict_tools(
        self,
    ) -> Dict[Literal['fetch_posts_tool', 'get_post_by_id_tool', 'get_post_by_slug_tool', 'create_post_tool'], StructuredTool]:
        return {
            'fetch_posts_tool': StructuredTool.from_function(
                coroutine=self.fetch_posts,
                description=self.__doc__,
                name='fetch_posts_tool',
            ),
            'get_post_by_id_tool': StructuredTool.from_function(
                coroutine=self.get_post_by_id,
                description=self.__doc__,
                name='get_post_by_id_tool',
            ),
            'get_post_by_slug_tool': StructuredTool.from_function(
                coroutine=self.get_post_by_slug,
                description=self.__doc__,
                name='get_post_by_slug_tool',
            ),
            'create_post_tool': StructuredTool.from_function(
                coroutine=self.create_post,
                description=self.__doc__,
                name='create_post_tool',
            ),
        }

    async def fetch_posts(self, params: PostListQueryParams | None = None) -> FetchPostsResult:
        """
        投稿一覧を取得します。
        検索キーワード、カテゴリ、タグ、作成者、日付範囲、ステータスなどで絞り込みが可能です。
        取得した投稿はタイトル、作成者、公開日時、カテゴリ、タグ、抜粋、URLなどの情報を含みます。
        ブログ記事のリサーチやコンテンツ分析に役立ちます。

        Args:
            params (PostListQueryParams | None): 投稿一覧取得のためのクエリパラメーター

        Returns:
            FetchPostsResult: 投稿データのリスト
        """
        result = await self.client.wp_fetch_posts(params=params.model_dump(exclude_none=True) if params else None)

        tasks = [self._parse_post_data(post) for post in result]
        posts = await asyncio.gather(*tasks)
        return FetchPostsResult(
            posts=posts,
            count=len(posts),
            message='Posts retrieved' if posts else 'No posts found',
        )

    async def get_post_by_id(self, post_id: int) -> PostSchema:
        """
        指定IDの投稿を取得します。
        取得した投稿はタイトル、作成者、公開日時、カテゴリ、タグ、抜粋、URLなどの情報を含みます。
        ブログ記事のリサーチやコンテンツ分析に役立ちます。

        Args:
            post_id (int): 取得したい投稿のID

        Returns:
            PostSchema: 取得した投稿データオブジェクト
        """
        post_data = await self.client.wp_get_post_by_id(post_id)
        return await self._parse_post_data(post_data)

    async def get_post_by_slug(self, slug: str) -> PostSchema:
        """
        指定スラッグの投稿を取得します。
        取得した投稿はタイトル、作成者、公開日時、カテゴリ、タグ、抜粋、URLなどの情報を含みます。
        ブログ記事のリサーチやコンテンツ分析に役立ちます。

        Args:
            slug (str): 取得したい投稿のスラッグ

        Returns:
            PostSchema: 取得した投稿データオブジェクト
        """
        post_data = await self.client.wp_get_post_by_slug(slug)
        return await self._parse_post_data(post_data)

    async def create_post(
        self,
        title: str,
        content: str,
        status: Literal['draft', 'publish'] = 'draft',
    ) -> PostSchema:
        """
        新しい投稿を作成します。
        返される投稿データには、タイトル、作成者、公開日時、カテゴリ、タグ、抜粋、URLなどの情報が含まれます。
        ブログ記事の作成やコンテンツ管理に役立ちます。

        Args:
            title (str): 投稿のタイトル
            content (str): 投稿の本文（HTML形式）
            status (Literal['draft', 'publish']): 投稿のステータス（draft または publish）

        Returns:
            PostSchema: 作成した投稿データオブジェクト
        """
        post_data = await self.client.wp_create_post(title=title, content=content, status=status)
        return await self._parse_post_data(post_data)

    async def _resolve_terms(self, term_type: Literal['categories', 'tags'], ids: List[int]) -> List[str]:
        """
        カテゴリまたはタグのIDリストから、それぞれの名前を取得します。

        Args:
            term_type (Literal['category', 'tag']): 取得する用語のタイプ（'category' または 'tag'）
            ids (List[int]): 取得したい用語のIDリスト

        Returns:
            List[str]: 用語の名前リスト
        """
        if not ids:
            return []

        result = await self.client.wp_fetch_items_by_ids(term_type, ids)
        return [item['name'] for item in result]

    async def _resolve_author(self, author_id: int) -> str:
        """
        作成者IDから作成者名を取得します。

        Args:
            author_id (int): 作成者のID

        Returns:
            str: 作成者名
        """
        user_data = await self.client.wp_get_user_by_id(author_id)
        return user_data.get('name') or user_data.get('slug') or 'No Name'

    async def _parse_post_data(self, post: dict[str, any]) -> PostSchema:
        """
        投稿データの辞書からPostSchemaオブジェクトを生成します。

        Args:
            post (dict): 投稿データの辞書

        Returns:
            PostSchema: 解析された投稿データオブジェクト
        """
        post_id = post['id']
        slug = post['slug']
        title = html2text.html2text(post['title']['rendered']).strip() if post.get('title') else 'No Title'
        date = datetime.fromisoformat(post['date'])
        content = html2text.html2text(post['content']['rendered']).strip() if post.get('content') else 'No Content'
        excerpt = html2text.html2text(post['excerpt']['rendered']).strip() if post.get('excerpt') else 'No Excerpt'
        url = post['link']
        status = post['status']

        resolve_tasks = {
            'author': self._resolve_author(post.get('author')),
            'categories': self._resolve_terms('categories', post.get('categories', [])),
            'tags': self._resolve_terms('tags', post.get('tags', [])),
        }
        resolved = await asyncio.gather(*resolve_tasks.values())
        author, categories, tags = resolved
        return PostSchema(
            id=post_id,
            slug=slug,
            title=title,
            author=author,
            date=date,
            categories=categories,
            tags=tags,
            content=content,
            excerpt=excerpt,
            url=url,
            status=status,
        )

    @classmethod
    def from_basic_auth(
        cls,
        base_url: str,
        username: str,
        app_password: str,
    ) -> 'WordPressToolManager':
        """
        ベーシック認証を使用してWordPressToolManagerのインスタンスを作成します。

        Args:
            base_url (str): WordPressサイトの基本URL（例: https://example.com）
            username (str): WordPressのユーザー名
            app_password (str): WordPressのアプリケーションパスワード

        Returns:
            WordPressToolManager: 認証されたWordPressToolManagerのインスタンス
        """
        client = WordPressBasicClient(
            base_url=base_url,
            username=username,
            app_password=app_password,
        )
        return cls(client=client)
