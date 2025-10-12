"""サイドバーコンポーネント"""

import streamlit as st


def render_sidebar():
    """サイドバーを描画する

    MCPサーバーパネルとLLM設定パネルを含むサイドバーを表示します。
    """
    with st.sidebar:
        # MCPサーバーパネル
        st.markdown('### MCP サーバー')

        if st.button('+ サーバー追加', key='add_server_button', use_container_width=True):
            st.info('サーバー追加機能は今後実装予定です')

        # サーバー一覧
        if 'mcp_servers' not in st.session_state:
            st.session_state.mcp_servers = []

        if len(st.session_state.mcp_servers) == 0:
            st.caption('サーバーが接続されていません')
        else:
            for server in st.session_state.mcp_servers:
                st.text(server)

        st.markdown('---')

        # LLM設定パネル
        st.markdown('### LLM 設定')

        # プロバイダー選択
        provider = st.selectbox(
            'プロバイダー',
            options=['Claude', 'GPT-4', 'Gemini'],
            key='llm_provider',
            help='LLMプロバイダーを選択',
        )

        # モデル選択（プロバイダーに応じて選択肢を変更）
        model_options = {
            'Claude': ['claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku'],
            'GPT-4': ['gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo'],
            'Gemini': ['gemini-pro', 'gemini-pro-vision'],
        }

        model = st.selectbox(
            'モデル',
            options=model_options.get(provider, []),
            key='llm_model',
            help='使用するモデルを選択',
        )

        # APIキー入力
        api_key = st.text_input(
            'APIキー',
            type='password',
            key='api_key',
            placeholder='APIキーを入力',
            help='LLMプロバイダーのAPIキーを入力してください',
        )

        # 接続ボタン
        connect_disabled = not api_key or len(api_key.strip()) == 0

        if st.button(
            '接続',
            key='connect_button',
            disabled=connect_disabled,
            use_container_width=True,
            type='primary',
        ):
            # 接続処理（今後実装）
            st.session_state.llm_connected = True
            st.session_state.selected_provider = provider
            st.session_state.selected_model = model
            st.success(f'✓ {provider} ({model}) に接続しました')

        # 接続状態の表示
        if st.session_state.get('llm_connected', False):
            st.caption(f"✓ 接続中: {st.session_state.get('selected_provider', '')} ({st.session_state.get('selected_model', '')})")
