"""
ヘッダーコンポーネント
アプリケーションタイトル・接続状態・設定ボタンを表示
"""

import streamlit as st


def render_header():
    """ヘッダー表示（Streamlitネイティブコンポーネント使用）"""

    # ヘッダーコンテナ
    header_container = st.container()

    with header_container:
        col1, col2, col3 = st.columns([6, 2, 1])

        with col1:
            st.title('🤖 MCP Assistant')
            st.caption('Model Context Protocol デモアプリケーション')

        with col2:
            # 接続状態表示
            st.success('🟢 接続中', icon='✅')

        with col3:
            # 設定ボタン（モーダル起動用）
            if st.button('⚙️', key='settings_btn', help='設定を開く'):
                st.session_state.show_settings_modal = True

        # 区切り線
        st.divider()
