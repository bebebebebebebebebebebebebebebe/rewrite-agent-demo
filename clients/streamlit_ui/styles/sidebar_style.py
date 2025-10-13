"""
サイドバースタイル設定
最小限のCSS注入でサイドバー幅を調整
"""


def get_sidebar_width_css(width: int = 320) -> str:
    """サイドバー幅設定のCSS

    Args:
        width: サイドバーの幅（px）デフォルト: 320

    Returns:
        CSS文字列
    """
    return f"""
    <style>
        /* サイドバー幅設定 */
        [data-testid="stSidebar"] {{
            min-width: {width}px;
            max-width: {width}px;
        }}

        [data-testid="stSidebar"] > div:first-child {{
            width: {width}px;
        }}

        /* レスポンシブ対応 */
        @media (max-width: 768px) {{
            [data-testid="stSidebar"] {{
                min-width: 100%;
                max-width: 100%;
            }}
        }}
    </style>
    """
