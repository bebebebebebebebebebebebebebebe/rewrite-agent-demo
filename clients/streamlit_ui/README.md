# MCP Assistant - Streamlit UI

Model Context Protocol デモアプリケーションのStreamlitベースUIです。

## 概要

このアプリケーションは、MCPサーバーとLLMの連携を可視化するためのデモUIです。
現在はモック実装となっており、実際のLLM/MCP連携機能は含まれていません。

## 特徴

- ✅ **Claude Desktop風デザイン**: 洗練されたUIデザイン
- ✅ **チャットインターフェース**: 直感的な会話型UI
- ✅ **プロセス可視化**: ツール実行プロセスのリアルタイム表示
- ✅ **MCPサーバー管理**: 複数サーバーの管理・追加
- ✅ **LLM設定**: 複数プロバイダー対応（Gemini, Claude, GPT-4）
- ✅ **レスポンシブ対応**: モバイル・タブレット・デスクトップ

## 起動方法

### 前提条件

- Python 3.11以上
- Streamlit 1.50.0以上

### インストール

プロジェクトルートで以下を実行:

```bash
# 依存関係インストール（プロジェクトルート）
uv sync
```

### 起動

```bash
# プロジェクトルートから実行
streamlit run clients/streamlit_ui/app.py

# または直接実行
cd clients/streamlit_ui
streamlit run app.py
```

アプリケーションが起動すると、ブラウザで `http://localhost:8501` が開きます。

## プロジェクト構造

```
clients/streamlit_ui/
├── .streamlit/
│   └── config.toml              # Streamlitテーマ設定
├── __init__.py
├── app.py                        # メインアプリケーション
├── mock_data.py                  # モックデータ定義
├── components/
│   ├── __init__.py
│   ├── header.py                # ヘッダーコンポーネント
│   ├── sidebar.py               # サイドバー（LLM設定・MCP管理）
│   ├── chat_area.py             # チャットエリア
│   └── process_viewer.py        # プロセス可視化
├── utils/
│   ├── __init__.py
│   └── session.py               # セッション状態管理
└── README.md
```

## 機能説明

### 1. ヘッダー

- アプリケーションタイトル
- 接続状態表示
- 設定ボタン

### 2. チャットエリア（メイン）

- メッセージ履歴表示
- ユーザー/アシスタントのメッセージ
- ツール呼び出し情報
- メッセージ入力フォーム

### 3. プロセス可視化エリア（右側）

- ツール実行ログのリアルタイム表示
- 実行状態（実行中/成功/エラー）
- 実行時間・パラメータ
- 折りたたみ可能

### 4. サイドバー

#### LLM設定

- プロバイダー選択（Gemini/Claude/GPT-4）
- APIキー入力
- モデル選択

#### MCPサーバー管理

- サーバー一覧表示
- 接続状態確認
- サーバー追加（モーダル）
- サーバー削除

## モックデータ

`mock_data.py`で定義されたダミーデータを使用:

- **会話履歴**: 初期メッセージ2件
- **MCPサーバー**: WordPress, GitHub, Notion（3件）
- **LLMプロバイダー**: Gemini, Claude, GPT-4

## カスタマイズ

### テーマ変更

`.streamlit/config.toml`でカラーテーマをカスタマイズ:

```toml
[theme]
primaryColor = "#5B5BD6"           # プライマリカラー
backgroundColor = "#FFFFFF"         # 背景色
secondaryBackgroundColor = "#F9F9FB" # セカンダリ背景色
textColor = "#2D2D2D"              # テキスト色
```

### モックデータ追加

`mock_data.py`でシナリオを追加:

```python
DEMO_SCENARIOS = {
    "your_scenario": {
        "user_message": "ユーザーメッセージ",
        "process": [...],
        "assistant_message": "アシスタント応答"
    }
}
```

## 今後の実装予定

- [ ] 実際のLLM連携（Gemini, Claude等）
- [ ] 実際のMCP連携（WordPress MCP等）
- [ ] ストリーミング応答
- [ ] エラーハンドリング
- [ ] 会話履歴の永続化
- [ ] ユーザー認証

## トラブルシューティング

### インポートエラーが発生する場合

プロジェクトルートから実行してください:

```bash
# プロジェクトルートで実行
streamlit run clients/streamlit_ui/app.py
```

または、PYTHONPATHを設定:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
streamlit run clients/streamlit_ui/app.py
```

### ポートが使用中の場合

別のポートで起動:

```bash
streamlit run clients/streamlit_ui/app.py --server.port 8502
```

## ライセンス

このプロジェクトはデモ目的で作成されています。

## 関連リンク

- [Streamlit公式ドキュメント](https://docs.streamlit.io/)
- [MCP公式サイト](https://modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp)
