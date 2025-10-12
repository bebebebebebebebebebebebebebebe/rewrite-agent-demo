"""MCP Assistant メインアプリケーション

Streamlitベースのユーザーインターフェースを提供します。
"""

import streamlit as st
from clients.streamlit_ui.components.chat_area import render_chat_area
from clients.streamlit_ui.components.header import render_header
from clients.streamlit_ui.components.process_viewer import render_process_viewer
from clients.streamlit_ui.components.sidebar import render_sidebar
from clients.streamlit_ui.styles.main_style import get_main_style


def main():
    """メインアプリケーション"""
    # ページ設定
    st.set_page_config(
        page_title='MCP Assistant',
        page_icon='💬',
        layout='wide',
        initial_sidebar_state='expanded',
    )

    # カスタムスタイルを適用
    st.markdown(get_main_style(), unsafe_allow_html=True)

    # ヘッダー
    render_header()

    # レイアウト: サイドバー、チャットエリア、プロセス可視化エリア
    # サイドバー
    render_sidebar()

    # メインエリア（チャットとプロセス可視化）
    main_col, process_col = st.columns([3, 1])

    with main_col:
        render_chat_area()

    with process_col:
        render_process_viewer()


if __name__ == '__main__':
    main()
