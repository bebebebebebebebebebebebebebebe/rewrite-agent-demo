"""
チャットエリアコンポーネント
メッセージ履歴表示・メッセージ入力・送信処理
"""

import time
from datetime import datetime

import streamlit as st
from clients.streamlit_ui.utils.session import add_message, add_process_log, update_latest_process_log


def render_chat_area():
    """チャットエリア表示"""

    st.subheader('💬 チャット')

    # メッセージ履歴表示エリア
    messages_container = st.container(height=500)

    with messages_container:
        for msg in st.session_state.messages:
            render_message(msg)

    # メッセージ入力
    user_input = st.chat_input('メッセージを入力してください...')

    if user_input:
        handle_user_message(user_input)


def render_message(msg: dict):
    """個別メッセージ表示

    Args:
        msg: メッセージ辞書（role, content, timestamp, tool_callsなど）
    """
    role = msg['role']
    content = msg['content']

    # Streamlitのst.chat_message使用
    with st.chat_message(role, avatar='👤' if role == 'user' else '🤖'):
        st.markdown(content)

        # タイムスタンプ
        if 'timestamp' in msg:
            st.caption(f"⏰ {msg['timestamp']}")

        # ツール呼び出し情報
        if 'tool_calls' in msg:
            for tool in msg['tool_calls']:
                render_tool_call(tool)


def render_tool_call(tool: dict):
    """ツール呼び出し情報表示（アシスタントメッセージ内に埋め込み）

    Args:
        tool: ツール呼び出し情報辞書
    """
    status_emoji = {'success': '✅', 'running': '⏳', 'error': '❌'}
    status_color = {'success': 'green', 'running': 'orange', 'error': 'red'}

    emoji = status_emoji.get(tool['status'], '⏳')
    color = status_color.get(tool['status'], 'gray')

    # ツール実行情報を目立つ形で表示
    with st.container(border=True):
        # ヘッダー行
        st.markdown(f"### 🔧 ツール実行: {tool['server']}")

        # ステータス行
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"**ツール名**  \n`{tool['tool']}`")

        with col2:
            st.markdown(f"**ステータス**  \n:{color}[{emoji} {tool['status']}]")

        with col3:
            if 'duration' in tool:
                st.markdown(f"**実行時間**  \n`{tool['duration']}`")
            else:
                st.markdown('**ステータス**  \n実行中...')

        # パラメータ表示（デフォルトで展開）
        if 'params' in tool:
            with st.expander('📋 パラメータを表示', expanded=True):
                st.json(tool['params'])

        # エラー表示
        if 'error' in tool:
            st.error(f"❌ エラー: {tool['error']}", icon='🚨')

        # 結果表示
        if 'result' in tool:
            st.success(f"✓ {tool['result']}", icon='✅')


def handle_user_message(user_input: str):
    """ユーザーメッセージ処理（モック）

    Args:
        user_input: ユーザー入力テキスト
    """
    # 現在時刻
    timestamp = datetime.now().strftime('%H:%M:%S')

    # ユーザーメッセージ追加
    add_message('user', user_input, timestamp=timestamp)

    # プロセスログ追加（実行中）
    add_process_log(
        server='WordPress MCP', tool='fetch_posts', status='running', start_time=timestamp, params={'query': user_input[:50]}
    )

    # 画面更新（ユーザーメッセージ表示）
    st.rerun()

    # モック処理（実際は非同期処理）
    time.sleep(0.5)

    # プロセスログ更新（成功）
    update_latest_process_log(status='success', duration='0.9s')

    # アシスタント応答
    add_message(
        'assistant',
        f'「{user_input}」についてのモック応答です。\n\n実際のLLM連携時には、リアルタイムで応答が生成されます。\n複数のMCPサーバーを使用して、様々な外部ツールと連携可能です。',
        timestamp=datetime.now().strftime('%H:%M:%S'),
        tool_calls=[
            {
                'server': 'WordPress MCP',
                'tool': 'fetch_posts',
                'status': 'success',
                'duration': '0.9s',
                'params': {'query': user_input[:50]},
            }
        ],
    )

    # 画面更新
    st.rerun()
