"""プロセス可視化エリアコンポーネント"""

import streamlit as st


def render_process_viewer():
    """プロセス可視化エリアを描画する

    実行ログを表示し、折りたたみ機能とクリア機能を提供します。
    """
    # セッション状態の初期化
    if 'process_logs' not in st.session_state:
        st.session_state.process_logs = []
    if 'process_viewer_collapsed' not in st.session_state:
        st.session_state.process_viewer_collapsed = False

    # ヘッダー
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        st.markdown('#### 実行ログ')

    with col2:
        # クリアボタン
        if st.button('🗑️', key='clear_logs_button', help='ログをクリア'):
            st.session_state.process_logs = []
            st.rerun()

    with col3:
        # 折りたたみボタン
        collapse_icon = '>' if st.session_state.process_viewer_collapsed else '<'
        if st.button(collapse_icon, key='toggle_process_viewer', help='折りたたみ'):
            st.session_state.process_viewer_collapsed = not st.session_state.process_viewer_collapsed
            st.rerun()

    # コンテンツエリア
    if not st.session_state.process_viewer_collapsed:
        st.markdown('---')

        if len(st.session_state.process_logs) == 0:
            st.caption('ツール実行はここに表示されます')
        else:
            # ログを表示
            for log in st.session_state.process_logs:
                st.text(log)
