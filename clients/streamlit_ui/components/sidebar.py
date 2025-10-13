"""
サイドバーコンポーネント
LLM設定・MCPサーバー管理
"""

import time

import streamlit as st
from clients.streamlit_ui.mock_data import LLM_PROVIDERS


def render_sidebar():
    """サイドバー表示"""

    with st.sidebar:
        # LLM設定セクション
        render_llm_settings()

        st.divider()

        # MCPサーバー管理セクション
        render_mcp_servers()

        st.divider()

        # デバッグモードトグル
        render_debug_toggle()


def render_llm_settings():
    """LLM設定パネル"""

    st.subheader('⚙️ LLM設定')

    with st.expander('設定を編集', expanded=False):
        # プロバイダー選択
        provider = st.selectbox(
            'プロバイダー',
            list(LLM_PROVIDERS.keys()),
            index=list(LLM_PROVIDERS.keys()).index(st.session_state.llm_provider),
            key='llm_provider_select',
        )

        # APIキー入力
        api_key = st.text_input(
            'APIキー',
            type='password',
            placeholder='sk-...',
            help='APIキーはセッション中のみ保持されます',
            value=st.session_state.llm_api_key,
        )

        # モデル選択（動的に変更）
        models = LLM_PROVIDERS.get(provider, [])

        # 現在のモデルがプロバイダーの選択肢にない場合は最初のモデルを選択
        current_model_index = 0
        if st.session_state.llm_model in models:
            current_model_index = models.index(st.session_state.llm_model)

        model = st.selectbox('モデル', models, index=current_model_index, key='llm_model_select')

        # 保存ボタン
        if st.button('💾 保存', type='primary', use_container_width=True):
            st.session_state.llm_provider = provider
            st.session_state.llm_model = model
            st.session_state.llm_api_key = api_key
            st.success('設定を保存しました', icon='✅')
            time.sleep(1)
            st.rerun()


def render_mcp_servers():
    """MCPサーバー管理パネル"""

    st.subheader('🔌 MCPサーバー')

    # サーバー一覧
    for server in st.session_state.mcp_servers:
        render_server_card(server)

    # サーバー追加ボタン
    if st.button('➕ サーバーを追加', use_container_width=True):
        show_add_server_dialog()


def render_server_card(server: dict):
    """個別サーバーカード表示

    Args:
        server: サーバー情報辞書
    """
    status_text = '接続中' if server['status'] == 'connected' else '切断'
    status_color = 'green' if server['status'] == 'connected' else 'red'

    with st.container(border=True):
        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown(f"### {server['icon']} {server['name']}")
            st.caption(f":{status_color}[{status_text}] • {server['tools_count']} ツール")

        with col2:
            # オプションメニュー
            with st.popover('⋮'):
                if st.button('詳細', key=f"detail_{server['name']}"):
                    st.info(f"接続タイプ: {server['connection_type']}\nツール数: {server['tools_count']}")

                if st.button('削除', key=f"delete_{server['name']}", type='secondary'):
                    st.warning('削除機能は未実装（モック）')


def render_debug_toggle():
    """デバッグモードトグル"""

    st.subheader('🔍 デバッグモード')

    # トグルスイッチ
    debug_enabled = st.toggle(
        'ツール実行ログを表示',
        value=st.session_state.show_process_viewer,
        help='開発者向け：全ツール実行の詳細ログを右側に表示',
        key='debug_toggle',
    )

    if debug_enabled != st.session_state.show_process_viewer:
        st.session_state.show_process_viewer = debug_enabled
        st.rerun()

    if debug_enabled:
        st.caption('✅ デバッグモード有効')
    else:
        st.caption('⚪ デバッグモード無効')


@st.dialog('サーバーを追加')
def show_add_server_dialog():
    """サーバー追加ダイアログ"""

    st.markdown('### 新しいMCPサーバーを追加')

    server_name = st.text_input('サーバー名', placeholder='例: GitHub MCP')

    connection_type = st.radio('接続タイプ', ['コマンド実行', 'HTTPエンドポイント'], horizontal=True)

    if connection_type == 'コマンド実行':
        _command = st.text_input('コマンド', placeholder='例: python -m github_mcp')
    else:
        _endpoint = st.text_input('エンドポイント', placeholder='例: http://localhost:8080')

    with st.expander('認証情報（任意）', expanded=False):
        auth_type = st.selectbox('認証タイプ', ['なし', 'APIキー', 'Bearer Token'])
        if auth_type != 'なし':
            _auth_value = st.text_input('認証情報', type='password')

    col1, col2 = st.columns(2)

    with col1:
        if st.button('キャンセル', use_container_width=True):
            st.rerun()

    with col2:
        if st.button('接続テスト', type='primary', use_container_width=True):
            if server_name:
                st.success('接続成功！（モック）', icon='✅')
                st.info('実際の実装では、ここでサーバー追加処理を行います')
            else:
                st.error('サーバー名を入力してください')
