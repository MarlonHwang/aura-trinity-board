import streamlit as st

def setup_style():
    """앱의 전반적인 스타일(CSS)을 정의합니다."""
    st.markdown("""
        <style>
        .stChatMessage { border-radius: 15px; }
        .stTextArea { border-radius: 10px; }
        /* 로그 화면 스타일 */
        .log-box {
            background-color: #0e1117;
            color: #00ff00;
            padding: 10px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            height: 400px;
            overflow-y: scroll;
            border: 1px solid #333;
        }
        </style>
    """, unsafe_allow_html=True)

def render_log_box(log_text):
    """로그 데이터를 터미널 스타일로 보여줍니다."""
    st.markdown(f'<div class="log-box"><pre>{log_text}</pre></div>', unsafe_allow_html=True)
