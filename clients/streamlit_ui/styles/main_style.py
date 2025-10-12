"""メインスタイル定義モジュール

MCP Assistant UIのカラースキーム、タイポグラフィ、レイアウトスタイルを定義します。
"""

# カラー定数
COLOR_PRIMARY = '#1E88E5'  # プライマリカラー（青）
COLOR_SECONDARY = '#F5F5F5'  # セカンダリカラー（薄いグレー）
COLOR_ERROR = '#D32F2F'  # エラーカラー（赤）
COLOR_SUCCESS = '#388E3C'  # 成功カラー（緑）
COLOR_BACKGROUND = '#FFFFFF'  # 背景色（白）
COLOR_TEXT = '#333333'  # テキストカラー（ダークグレー）
COLOR_BORDER = '#E0E0E0'  # ボーダーカラー（薄いグレー）

# サイズ定数
HEADER_HEIGHT = 60  # ヘッダーの高さ（px）
SIDEBAR_WIDTH = 250  # サイドバーの幅（px）
PROCESS_VIEWER_WIDTH = 300  # プロセス可視化エリアの幅（px）
BUTTON_MIN_SIZE = 44  # ボタンの最小サイズ（px）


def get_main_style() -> str:
    """メインスタイルのCSS文字列を返す

    Returns:
        str: CSS文字列
    """
    return f"""
    <style>
        /* グローバルスタイル */
        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif;
            line-height: 1.5;
            color: {COLOR_TEXT};
            background-color: {COLOR_BACKGROUND};
        }}

        /* ヘッダースタイル */
        .header {{
            height: {HEADER_HEIGHT}px;
            background-color: {COLOR_BACKGROUND};
            border-bottom: 1px solid {COLOR_BORDER};
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 24px;
        }}

        .header-title {{
            font-size: 24px;
            font-weight: 600;
            color: {COLOR_TEXT};
        }}

        .header-settings-icon {{
            font-size: 24px;
            cursor: pointer;
            transition: opacity 0.2s;
        }}

        .header-settings-icon:hover {{
            opacity: 0.7;
        }}

        /* サイドバースタイル */
        .sidebar {{
            width: {SIDEBAR_WIDTH}px;
            background-color: {COLOR_SECONDARY};
            padding: 16px;
            height: calc(100vh - {HEADER_HEIGHT}px);
            overflow-y: auto;
        }}

        .sidebar-section {{
            margin-bottom: 24px;
        }}

        .sidebar-section-title {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 12px;
            color: {COLOR_TEXT};
        }}

        /* ボタンスタイル */
        .button-primary {{
            background-color: {COLOR_PRIMARY};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            min-height: {BUTTON_MIN_SIZE}px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s;
        }}

        .button-primary:hover {{
            opacity: 0.9;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}

        .button-primary:disabled {{
            background-color: {COLOR_BORDER};
            cursor: not-allowed;
            opacity: 0.6;
        }}

        /* 入力フィールドスタイル */
        .input-field {{
            width: 100%;
            padding: 8px 12px;
            border: 1px solid {COLOR_BORDER};
            border-radius: 4px;
            font-size: 14px;
            transition: border-color 0.2s;
        }}

        .input-field:focus {{
            outline: none;
            border-color: {COLOR_PRIMARY};
            box-shadow: 0 0 0 2px rgba(30, 136, 229, 0.1);
        }}

        /* チャットエリアスタイル */
        .chat-area {{
            flex: 1;
            display: flex;
            flex-direction: column;
            background-color: {COLOR_BACKGROUND};
            height: calc(100vh - {HEADER_HEIGHT}px);
        }}

        .welcome-message {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 48px 24px;
            color: {COLOR_TEXT};
        }}

        .welcome-icon {{
            font-size: 48px;
            margin-bottom: 16px;
        }}

        .welcome-title {{
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 16px;
        }}

        .welcome-guide {{
            max-width: 600px;
            text-align: left;
            margin-top: 24px;
        }}

        .welcome-guide-step {{
            margin-bottom: 12px;
            padding-left: 24px;
        }}

        /* メッセージ入力フォームスタイル */
        .message-input-form {{
            border-top: 1px solid {COLOR_BORDER};
            padding: 16px 24px;
            background-color: {COLOR_BACKGROUND};
        }}

        .message-input-container {{
            display: flex;
            align-items: flex-end;
            gap: 8px;
        }}

        .message-textarea {{
            flex: 1;
            min-height: 44px;
            max-height: 120px;
            resize: vertical;
            padding: 10px 12px;
            border: 1px solid {COLOR_BORDER};
            border-radius: 4px;
            font-size: 14px;
            font-family: inherit;
        }}

        .message-textarea:focus {{
            outline: none;
            border-color: {COLOR_PRIMARY};
            box-shadow: 0 0 0 2px rgba(30, 136, 229, 0.1);
        }}

        .send-button {{
            min-width: {BUTTON_MIN_SIZE}px;
            min-height: {BUTTON_MIN_SIZE}px;
            background-color: {COLOR_PRIMARY};
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 18px;
            transition: all 0.2s;
        }}

        .send-button:hover {{
            opacity: 0.9;
        }}

        .send-button:disabled {{
            background-color: {COLOR_BORDER};
            cursor: not-allowed;
            opacity: 0.6;
        }}

        /* プロセス可視化エリアスタイル */
        .process-viewer {{
            width: {PROCESS_VIEWER_WIDTH}px;
            background-color: {COLOR_SECONDARY};
            border-left: 1px solid {COLOR_BORDER};
            height: calc(100vh - {HEADER_HEIGHT}px);
            display: flex;
            flex-direction: column;
        }}

        .process-viewer-header {{
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 12px;
            border-bottom: 1px solid {COLOR_BORDER};
            background-color: {COLOR_BACKGROUND};
        }}

        .process-viewer-title {{
            font-size: 14px;
            font-weight: 600;
            color: {COLOR_TEXT};
        }}

        .process-viewer-actions {{
            display: flex;
            gap: 8px;
        }}

        .icon-button {{
            background: none;
            border: none;
            cursor: pointer;
            font-size: 16px;
            padding: 4px;
            transition: opacity 0.2s;
        }}

        .icon-button:hover {{
            opacity: 0.7;
        }}

        .process-viewer-content {{
            flex: 1;
            overflow-y: auto;
            padding: 12px;
        }}

        .process-viewer-content.collapsed {{
            display: none;
        }}

        .process-viewer-empty {{
            color: #999;
            font-size: 14px;
            text-align: center;
            padding: 24px 12px;
        }}

        /* ユーティリティクラス */
        .text-error {{
            color: {COLOR_ERROR};
        }}

        .text-success {{
            color: {COLOR_SUCCESS};
        }}

        .mt-8 {{
            margin-top: 8px;
        }}

        .mt-16 {{
            margin-top: 16px;
        }}

        .mb-8 {{
            margin-bottom: 8px;
        }}

        .mb-16 {{
            margin-bottom: 16px;
        }}
    </style>
    """
