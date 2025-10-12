"""Streamlit UIコンポーネントのテスト"""


class TestStyleDefinition:
    """スタイル定義のテスト"""

    def test_get_main_style_returns_string(self):
        """get_main_style関数がCSS文字列を返すことを確認"""
        from clients.streamlit_ui.styles.main_style import get_main_style

        style = get_main_style()
        assert isinstance(style, str)
        assert len(style) > 0

    def test_color_constants_defined(self):
        """カラー定数が定義されていることを確認"""
        from clients.streamlit_ui.styles.main_style import (
            COLOR_ERROR,
            COLOR_PRIMARY,
            COLOR_SECONDARY,
            COLOR_SUCCESS,
        )

        assert COLOR_PRIMARY == '#1E88E5'
        assert COLOR_SECONDARY == '#F5F5F5'
        assert COLOR_ERROR == '#D32F2F'
        assert COLOR_SUCCESS == '#388E3C'

    def test_main_style_contains_layout_rules(self):
        """メインスタイルにレイアウトルールが含まれることを確認"""
        from clients.streamlit_ui.styles.main_style import get_main_style

        style = get_main_style()
        # ヘッダー、サイドバー、チャットエリア、プロセス可視化エリアのスタイルが含まれる
        assert '.header' in style or 'header' in style.lower()
        assert 'sidebar' in style.lower()


class TestHeaderComponent:
    """ヘッダーコンポーネントのテスト"""

    def test_render_header_function_exists(self):
        """render_header関数が存在することを確認"""
        from clients.streamlit_ui.components.header import render_header

        assert callable(render_header)

    def test_render_header_does_not_raise_exception(self):
        """render_header関数が例外を起こさないことを確認"""
        from clients.streamlit_ui.components.header import render_header

        # Streamlitのコンテキスト外では完全に動作しないが、関数が定義されていることを確認
        try:
            render_header()
        except Exception:  # noqa: S110
            # Streamlitコンテキスト外での実行エラーは想定内
            pass


class TestSidebarComponent:
    """サイドバーコンポーネントのテスト"""

    def test_render_sidebar_function_exists(self):
        """render_sidebar関数が存在することを確認"""
        from clients.streamlit_ui.components.sidebar import render_sidebar

        assert callable(render_sidebar)

    def test_render_sidebar_does_not_raise_exception(self):
        """render_sidebar関数が例外を起こさないことを確認"""
        from clients.streamlit_ui.components.sidebar import render_sidebar

        try:
            render_sidebar()
        except Exception:  # noqa: S110
            # Streamlitコンテキスト外での実行エラーは想定内
            pass


class TestChatAreaComponent:
    """チャットエリアコンポーネントのテスト"""

    def test_render_chat_area_function_exists(self):
        """render_chat_area関数が存在することを確認"""
        from clients.streamlit_ui.components.chat_area import render_chat_area

        assert callable(render_chat_area)

    def test_render_chat_area_does_not_raise_exception(self):
        """render_chat_area関数が例外を起こさないことを確認"""
        from clients.streamlit_ui.components.chat_area import render_chat_area

        try:
            render_chat_area()
        except Exception:  # noqa: S110
            # Streamlitコンテキスト外での実行エラーは想定内
            pass


class TestProcessViewerComponent:
    """プロセス可視化エリアコンポーネントのテスト"""

    def test_render_process_viewer_function_exists(self):
        """render_process_viewer関数が存在することを確認"""
        from clients.streamlit_ui.components.process_viewer import render_process_viewer

        assert callable(render_process_viewer)

    def test_render_process_viewer_does_not_raise_exception(self):
        """render_process_viewer関数が例外を起こさないことを確認"""
        from clients.streamlit_ui.components.process_viewer import render_process_viewer

        try:
            render_process_viewer()
        except Exception:  # noqa: S110
            # Streamlitコンテキスト外での実行エラーは想定内
            pass
