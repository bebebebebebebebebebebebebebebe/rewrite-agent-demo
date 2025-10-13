"""
セッション状態管理
Streamlitのst.session_stateを初期化・管理
"""

import streamlit as st
from clients.streamlit_ui.mock_data import MOCK_CONVERSATIONS, MOCK_MCP_SERVERS


def initialize_session():
    """セッション状態の初期化"""

    # 会話履歴
    if 'messages' not in st.session_state:
        st.session_state.messages = MOCK_CONVERSATIONS[:2]  # 初期メッセージ2件

    # MCPサーバー一覧
    if 'mcp_servers' not in st.session_state:
        st.session_state.mcp_servers = MOCK_MCP_SERVERS.copy()

    # プロセスログ
    if 'process_logs' not in st.session_state:
        st.session_state.process_logs = []

    # LLM設定
    if 'llm_provider' not in st.session_state:
        st.session_state.llm_provider = 'Google Gemini'

    if 'llm_model' not in st.session_state:
        st.session_state.llm_model = 'gemini-2.0-flash-exp'

    if 'llm_api_key' not in st.session_state:
        st.session_state.llm_api_key = ''

    # UI状態
    if 'show_process_viewer' not in st.session_state:
        st.session_state.show_process_viewer = False  # デバッグモード：デフォルト非表示

    if 'show_settings_modal' not in st.session_state:
        st.session_state.show_settings_modal = False


def clear_session():
    """セッション状態のクリア"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def add_message(role: str, content: str, **kwargs):
    """メッセージを追加

    Args:
        role: 'user' or 'assistant'
        content: メッセージ内容
        **kwargs: 追加情報（timestamp, tool_callsなど）
    """
    message = {'role': role, 'content': content}
    message.update(kwargs)
    st.session_state.messages.append(message)


def add_process_log(server: str, tool: str, status: str = 'running', **kwargs):
    """プロセスログを追加

    Args:
        server: サーバー名
        tool: ツール名
        status: 'running', 'success', 'error'
        **kwargs: 追加情報（duration, paramsなど）
    """
    log_id = len(st.session_state.process_logs) + 1
    log = {'id': log_id, 'server': server, 'tool': tool, 'status': status}
    log.update(kwargs)
    st.session_state.process_logs.append(log)


def update_latest_process_log(**kwargs):
    """最新のプロセスログを更新

    Args:
        **kwargs: 更新する情報（status, durationなど）
    """
    if st.session_state.process_logs:
        st.session_state.process_logs[-1].update(kwargs)
