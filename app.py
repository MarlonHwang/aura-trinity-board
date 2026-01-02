import streamlit as st
from modules import gemini_brain, nexus_bridge, ui_components

st.set_page_config(page_title="AURA TRINITY", layout="wide")
ui_components.setup_style()

# --- [사이드바 설정] ---
with st.sidebar:
    st.title("🎛️ AURA CONTROL")
    
    st.subheader("🧠 AI Brain Select")
    model_option = st.selectbox(
        "사용할 모델을 선택하세요:",
        (
            "gemini-3-flash-preview",    # [공식] Gemini 3 Flash (무료 티어 지원)
            "gemini-3-pro-preview",      # [공식] Gemini 3 Pro (유료 가능성 있음)
            "gemini-2.0-flash-exp",      # 2.0 실험 버전
            "gemini-1.5-flash"           # 구버전 (비상용)
        ),
        index=0 # 기본값을 무료인 'Gemini 3 Flash'로 설정
    )
    
    # 모델명 직접 입력 기능 (혹시 모를 상황 대비)
    use_custom = st.checkbox("직접 모델명 입력")
    if use_custom:
        model_option = st.text_input("모델명 입력", value=model_option)

    st.info(f"선택된 두뇌: {model_option}")
    st.markdown("---")
    
    gist_url = st.text_input("🔗 Gist Raw URL")
    if st.button("🔄 시스템 재가동"):
        st.rerun()

# --- [메인 로직] ---
if "gemini_ready" not in st.session_state:
    st.session_state.gemini_ready = gemini_brain.init_gemini()

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📡 LOCAL AGENT LOG")
    if gist_url:
        log_data = nexus_bridge.get_nexus_log(gist_url)
        ui_components.render_log_box(log_data)
    else:
        st.info("👈 Gist URL을 입력하세요.")

with col2:
    st.subheader("💬 COMMAND CENTER")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("명령을 입력하세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        if st.session_state.gemini_ready:
            with st.chat_message("assistant"):
                with st.spinner(f"Thinking with {model_option}..."):
                    # [핵심] 선택한 model_option을 전달
                    history_context = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages if m["role"] != "system"]
                    response = gemini_brain.get_response(history_context, prompt, model_name=model_option)
                    st.write(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
