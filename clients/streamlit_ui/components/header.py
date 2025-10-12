"""ヘッダーコンポーネント"""

import streamlit as st


def render_header():
    """ヘッダーを描画する

    アプリケーション名と設定アイコンを含むヘッダーを表示します。
    """
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown('## MCP Assistant')

    with col2:
        if st.button('⚙️', key='settings_button', help='設定'):
            st.info('設定機能は今後実装予定です')
