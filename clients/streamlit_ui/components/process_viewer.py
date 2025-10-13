"""
プロセスビューアコンポーネント
ツール実行プロセスのリアルタイム可視化
"""

import streamlit as st


def render_process_viewer():
    """プロセス可視化エリア表示（デバッグモード）"""

    # ヘッダー
    st.subheader('🔍 デバッグモード: ツール実行ログ')
    st.caption('開発者向け：全ツール実行の詳細ログを時系列で表示')

    st.divider()

    # プロセスログ表示
    if not st.session_state.process_logs:
        st.info('ツール実行ログはここに表示されます', icon='ℹ️')
        st.markdown("""
        **デバッグモードについて:**
        - チャット内に表示されたツール実行の詳細ログ
        - 開発・デバッグ時に有用
        - 本番環境では非表示推奨
        """)
        return

    # 統計情報
    total_logs = len(st.session_state.process_logs)
    success_count = sum(1 for log in st.session_state.process_logs if log['status'] == 'success')
    error_count = sum(1 for log in st.session_state.process_logs if log['status'] == 'error')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('総実行数', total_logs)
    with col2:
        st.metric('成功', success_count, delta=None, delta_color='normal')
    with col3:
        st.metric('エラー', error_count, delta=None, delta_color='inverse')

    st.divider()

    # ログコンテナ（スクロール可能）
    logs_container = st.container(height=400)

    with logs_container:
        for log in st.session_state.process_logs:
            render_process_card(log)


def render_process_card(log: dict):
    """個別プロセスカード表示

    Args:
        log: プロセスログ辞書
    """
    status_config = {
        'running': {'emoji': '⏳', 'color': 'orange', 'text': '実行中'},
        'success': {'emoji': '✅', 'color': 'green', 'text': '成功'},
        'error': {'emoji': '❌', 'color': 'red', 'text': 'エラー'},
    }

    config = status_config.get(log['status'], status_config['running'])

    # st.status使用（Streamlitネイティブ）
    status_state = 'running' if log['status'] == 'running' else 'complete'
    status_label = f"{config['emoji']} {log['server']} → {log['tool']}"

    with st.status(status_label, state=status_state, expanded=False):
        # メトリクス表示
        col1, col2 = st.columns(2)

        with col1:
            st.metric('開始時刻', log.get('start_time', '-'))

        with col2:
            if 'duration' in log:
                st.metric('実行時間', log['duration'])
            else:
                st.metric('ステータス', '実行中...')

        # パラメータ表示
        if 'params' in log:
            st.markdown('**パラメータ:**')
            st.json(log['params'])

        # エラー情報
        if 'error' in log:
            st.error(f"エラー: {log['error']}")

        # 結果情報
        if 'result' in log:
            st.success(f"結果: {log['result']}")
