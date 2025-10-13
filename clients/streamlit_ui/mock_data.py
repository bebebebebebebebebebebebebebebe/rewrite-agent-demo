"""
モックデータ定義
デモ・UIテスト用のダミーデータ
"""

# 会話履歴のモックデータ
MOCK_CONVERSATIONS = [
    {
        'role': 'user',
        'content': '最新のブログ記事5件を取得して要約してください',
        'timestamp': '14:30:00',
    },
    {
        'role': 'assistant',
        'content': """WordPress MCPサーバーから記事を取得しました。

以下、最新記事5件の要約です：

1. **MCPプロトコル入門** (2025-10-10)
   - Model Context Protocolの基礎概念を解説
   - 外部ツールとLLMの連携方法について詳説

2. **Streamlit開発Tips** (2025-10-08)
   - カスタムコンポーネントの作成方法
   - パフォーマンス最適化テクニック

3. **LangChain v0.3新機能** (2025-10-05)
   - LangGraphの強化ポイント
   - エージェント開発の新パターン

4. **Python 3.13リリース** (2025-10-03)
   - パフォーマンス改善の詳細
   - 新しい構文機能の紹介

5. **FastAPI vs Flask比較** (2025-10-01)
   - ベンチマーク結果
   - ユースケース別推奨""",
        'timestamp': '14:30:05',
        'tool_calls': [
            {
                'server': 'WordPress MCP',
                'tool': 'fetch_posts',
                'status': 'success',
                'duration': '1.2s',
                'params': {'per_page': 5, 'orderby': 'date', 'order': 'desc'},
            }
        ],
    },
]

# MCPサーバーのモックデータ
MOCK_MCP_SERVERS = [
    {
        'name': 'WordPress MCP',
        'status': 'connected',
        'connection_type': 'command',
        'tools_count': 5,
        'icon': '📝',
    },
    {
        'name': 'GitHub MCP',
        'status': 'connected',
        'connection_type': 'http',
        'tools_count': 8,
        'icon': '🐙',
    },
    {
        'name': 'Notion MCP',
        'status': 'disconnected',
        'connection_type': 'command',
        'tools_count': 0,
        'icon': '📓',
    },
]

# LLMプロバイダーとモデルの設定
LLM_PROVIDERS = {
    'Google Gemini': ['gemini-2.0-flash-exp', 'gemini-1.5-pro', 'gemini-1.5-flash'],
    'Anthropic Claude': ['claude-3-5-sonnet-20241022', 'claude-3-opus-20240229', 'claude-3-haiku-20240307'],
    'OpenAI GPT-4': ['gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo'],
}

# デモ用のプリセットシナリオ
DEMO_SCENARIOS = {
    'wordpress_fetch': {
        'user_message': '最新のブログ記事を5件取得してください',
        'process': [
            {'server': 'WordPress MCP', 'tool': 'fetch_posts', 'duration': '1.2s', 'status': 'success'},
        ],
        'assistant_message': """5件の記事を取得しました：

1. MCPプロトコル入門
2. Streamlit開発Tips
3. LangChain v0.3新機能
4. Python 3.13リリース
5. FastAPI vs Flask比較""",
    },
    'multi_tool': {
        'user_message': 'GitHubのissueとWordPress記事を両方確認したい',
        'process': [
            {'server': 'GitHub MCP', 'tool': 'fetch_issues', 'duration': '0.8s', 'status': 'success'},
            {'server': 'WordPress MCP', 'tool': 'fetch_posts', 'duration': '1.1s', 'status': 'success'},
        ],
        'assistant_message': """両方のデータを取得しました。

**GitHub Issues (5件):**
- Feature request: ダークモード対応
- Bug: ログイン時のエラー
- Enhancement: パフォーマンス改善
- Documentation: README更新
- Question: API使用方法

**WordPress記事 (3件):**
- 最新の技術トレンド
- 開発Tips集
- プロジェクト管理手法""",
    },
    'error_case': {
        'user_message': '存在しない記事ID=9999を取得して',
        'process': [
            {
                'server': 'WordPress MCP',
                'tool': 'get_post_by_id',
                'status': 'error',
                'error': '404 Not Found',
                'duration': '0.3s',
            },
        ],
        'assistant_message': """エラーが発生しました。

記事ID 9999 は存在しません。有効な記事IDを指定してください。""",
    },
}
