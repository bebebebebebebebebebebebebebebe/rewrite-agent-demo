"""チャットエリアコンポーネント"""

import streamlit as st


def render_chat_area():
    """チャットエリアを描画する

    ウェルカムメッセージ、メッセージ表示エリア、メッセージ入力フォームを表示します。
    """
    # セッション状態の初期化
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'llm_connected' not in st.session_state:
        st.session_state.llm_connected = False

    # メッセージが空の場合、ウェルカムメッセージを表示
    if len(st.session_state.messages) == 0:
        _render_welcome_message()
    else:
        # メッセージ履歴を表示
        for message in st.session_state.messages:
            with st.chat_message(message['role']):
                st.markdown(message['content'])

    # メッセージ入力フォーム
    _render_message_input_form()


def _render_welcome_message():
    """ウェルカムメッセージを描画する"""
    st.markdown(
        """
    <div style='text-align: center; padding: 48px 24px;'>
        <div style='font-size: 48px; margin-bottom: 16px;'>💬</div>
        <h1 style='font-size: 28px; font-weight: 600; margin-bottom: 16px;'>こんにちは！</h1>
        <p>MCP Assistantへようこそ。以下の手順で始めましょう：</p>
        <div style='max-width: 600px; margin: 24px auto; text-align: left;'>
            <p><strong>1. サイドバーでLLMを設定</strong></p>
            <p style='margin-left: 24px; color: #666;'>プロバイダー、モデル、APIキーを入力して接続してください。</p>
            <p><strong>2. MCPサーバーを追加（オプション）</strong></p>
            <p style='margin-left: 24px; color: #666;'>必要に応じてMCPサーバーを接続できます。</p>
            <p><strong>3. メッセージを送信</strong></p>
            <p style='margin-left: 24px; color: #666;'>下のテキストボックスからメッセージを入力して送信してください。</p>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def _render_message_input_form():
    """メッセージ入力フォームを描画する"""
    # LLM接続状態をチェック
    llm_connected = st.session_state.get('llm_connected', False)

    if not llm_connected:
        st.info('💡 メッセージを送信するには、サイドバーでLLMを接続してください。')
        return

    # チャット入力
    prompt = st.chat_input('メッセージを入力...', key='chat_input')

    if prompt:
        # ユーザーメッセージを追加
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        # アシスタントの応答（ダミー）
        # 実際の実装では、ここでLLM APIを呼び出します
        response = f'「{prompt}」というメッセージを受け取りました。\n\n（この応答はダミーです。実際のLLM連携は今後実装予定です。）'
        st.session_state.messages.append({'role': 'assistant', 'content': response})

        # 再描画のためにリラン
        st.rerun()
