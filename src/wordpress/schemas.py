from datetime import datetime
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field


class PostAuthor(BaseModel):
    id: int = Field(description='投稿作成者の一意なID')
    name: str = Field(description='投稿作成者の表示名')


class PostSchema(BaseModel):
    id: int = Field(description='WordPressで割り当てられる投稿の一意なID')
    slug: str = Field(description='URLの一部として使用される投稿スラッグ（短い識別子）')
    title: str = Field(description='投稿のタイトル（HTMLタグを除去したテキスト）')
    author: PostAuthor = Field(description='投稿の作成者情報')
    date: datetime = Field(description='投稿の公開日時（ISO 8601形式）')
    categories: List[str] = Field(description='投稿に紐づけられたカテゴリ名のリスト')
    tags: List[str] = Field(description='投稿に付与されたタグのリスト')
    content: str = Field(description='投稿本文のテキスト（HTMLを除去したもの）')
    excerpt: str = Field(description='投稿本文の抜粋（要約や冒頭部分）')
    url: str = Field(description='投稿の公開URL')
    status: Literal['draft', 'publish'] = Field(description='投稿のステータス（draft または publish）', default='draft')


class FetchPostsResult(BaseModel):
    posts: List[PostSchema] = Field(description='取得した投稿のリスト')
    count: int = Field(description='取得した投稿の総数')
    message: Literal['Posts retrieved', 'No posts found'] = Field(description='操作の結果メッセージ')


class WPPreviousPost(BaseModel):
    id: int = Field(description='削除前の投稿の一意なID')
    date: Optional[str] = Field(description='削除前の投稿の公開日時（ISO 8601形式）')
    slug: str = Field(description='削除前の投稿のスラッグ')
    status: str = Field(description='削除前の投稿のステータス')
    type: str = Field(description='削除前の投稿のタイプ')
    title: str = Field(description='削除前の投稿のタイトル')
    content: Optional[str] = Field(description='削除前の投稿の本文')
    author: Optional[PostAuthor] = Field(description='削除前の投稿の作成者情報')
    link: Optional[str] = Field(description='削除前の投稿のリンクURL')


class DeletePostResult(BaseModel):
    deleted: bool = Field(description='投稿が削除されたかどうか')
    previous: Optional[WPPreviousPost] = Field(description='削除前の投稿データ')


class PostListQueryParams(BaseModel):
    """投稿一覧取得のためのクエリパラメーター"""

    page: Optional[int] = Field(default=1, ge=1, description='取得するページ番号（1始まり、1以上）')
    per_page: Optional[int] = Field(default=10, ge=1, le=100, description='1ページあたりの投稿数（最大 100 件）')
    search: Optional[str] = Field(default=None, description='投稿タイトル・本文等を対象とする全文検索キーワード')
    after: Optional[datetime] = Field(default=None, description='指定日時以降に公開された投稿に絞る（ISO 8601 形式）')
    before: Optional[datetime] = Field(default=None, description='指定日時以前に公開された投稿に絞る（ISO 8601 形式）')
    modified_after: Optional[datetime] = Field(default=None, description='指定日時以降に修正された投稿に絞る（ISO 8601 形式）')
    modified_before: Optional[datetime] = Field(default=None, description='指定日時以前に修正された投稿に絞る（ISO 8601 形式）')
    author: Optional[Union[int, List[int]]] = Field(default=None, description='投稿の作成者 ID で絞る（単一 ID または ID のリスト）')
    author_exclude: Optional[Union[int, List[int]]] = Field(default=None, description='除外したい作成者 ID（単一または複数）')
    include: Optional[Union[int, List[int]]] = Field(default=None, description='対象とする投稿 ID（単一または複数）')
    exclude: Optional[Union[int, List[int]]] = Field(default=None, description='除外する投稿 ID（単一または複数）')
    slug: Optional[Union[str, List[str]]] = Field(default=None, description='投稿スラッグで絞る（単一または複数）')
    status: Optional[Union[str, List[str]]] = Field(
        default='publish', description='投稿ステータス（例: publish, draft, private など）'
    )
    categories: Optional[Union[int, List[int]]] = Field(default=None, description='カテゴリ ID で絞る（単一または複数）')
    categories_exclude: Optional[Union[int, List[int]]] = Field(default=None, description='除外するカテゴリ ID（単一または複数）')
    tags: Optional[Union[int, List[int]]] = Field(default=None, description='タグ ID で絞る（単一または複数）')
    format: Optional[str] = Field(default=None, description='投稿フォーマット（例: standard, aside, gallery, …）')
    orderby: Optional[str] = Field(default='date', description='ソート対象フィールド（例: date, id, title, modified, slug 等）')
    order: Optional[str] = Field(default='desc', description='ソート順（asc：昇順 / desc：降順）')
    sticky: Optional[bool] = Field(default=None, description='スティッキーポストかどうかで絞る（true または false）')


class CreatePostArgs(BaseModel):
    title: str = Field(description='投稿のタイトル')
    content: str = Field(description='投稿の本文（HTML形式）')
    status: Literal['draft', 'publish'] = Field(default='draft', description='投稿のステータス（draft または publish）')
