"""
MCP Assistant - メインアプリケーション
Model Context Protocol デモ用Streamlit UI（モック版）
"""

import streamlit as st
from clients.streamlit_ui.components.chat_area import render_chat_area
from clients.streamlit_ui.components.header import render_header
from clients.streamlit_ui.components.process_viewer import render_process_viewer
from clients.streamlit_ui.components.sidebar import render_sidebar
from clients.streamlit_ui.styles.sidebar_style import get_sidebar_width_css
from clients.streamlit_ui.utils.session import initialize_session

# ページ設定
st.set_page_config(
    page_title='MCP Assistant',
    page_icon='🤖',
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={'About': 'MCP Assistant - Model Context Protocol デモアプリケーション'},
)

# サイドバー幅設定（カスタムCSS）
st.markdown(get_sidebar_width_css(320), unsafe_allow_html=True)

# セッション初期化
initialize_session()

# ヘッダー
render_header()

# メインレイアウト（デバッグモードで条件分岐）
if st.session_state.show_process_viewer:
    # デバッグモード有効：2カラムレイアウト
    col_main, col_process = st.columns([3, 2], gap='medium')

    with col_main:
        render_chat_area()

    with col_process:
        render_process_viewer()
else:
    # デバッグモード無効：1カラムレイアウト（チャットのみ）
    render_chat_area()

# サイドバー
render_sidebar()

# フッター
st.markdown('---')
st.caption('💡 これはデモUIです。実際のLLM/MCP連携機能は未実装です。')
