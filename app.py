import streamlit as st
import requests
import modules.gemini_brain as brain

# ==========================================
# [CONFIG] 시스템 설정 및 좌표
# ==========================================
# CEO가 하달한 Nexus(Gist) 접선 장소
NEXUS_URL_RAW = "https://gist.githubusercontent.com/MarlonHwang/0a8e7897456df5e6302830dab5390c06/raw"

st.set_page_config(
    page_title="AURA TRINITY v2.3",
    page_icon="�",
    layout="wide"
)

# ==========================================
# [SIDEBAR] 상태창 & 설정
# ==========================================
with st.sidebar:
    st.title("👁️ TRINITY CONTROL")
    st.caption("Hybrid Communication Hub")
    
    # [복구] Model Selector
    st.subheader("🧠 AI Brain Select")
    model_option = st.selectbox(
        "사용할 모델을 선택하세요:",
        (
            "gemini-2.0-flash-exp",     # [추천] 가장 빠르고 똑똑함
            "gemini-1.5-flash",          # [안정] 안정적인 버전
            "gemini-1.5-pro",            # [고성능]
            "gemini-3-flash-preview"     # [실험]
        ),
        index=0
    )
    st.caption(f"🚀 System Version: v2.3 (Visual Check)")
    st.toast("🔥 System Updated to v2.3!")
    
    # 연결 상태 확인 및 초기화
    if "gemini" in st.secrets:
        if brain.init_gemini():
            st.success("🟢 AI Neural Net: Online")
        else:
            st.error("🔴 AI Neural Net: Error")
    else:
        st.error("🔴 AI Neural Net: Offline")

    if st.button("🔄 시스템 새로고침"):
        st.rerun()

# ==========================================
# [MAIN] 탭 레이아웃 (Monitor & Command)
# ==========================================
tab1, tab2 = st.tabs(["📡 MONITOR (Nexus)", "💬 COMMAND (Gemini)"])

# ------------------------------------------
# TAB 1: NEXUS MONITOR (상황 관제)
# ------------------------------------------
with tab1:
    st.subheader("📡 Real-time Operation Log")
    try:
        # Gist에서 실시간 로그 긁어오기 (캐시 방지용 파라미터 추가)
        response = requests.get(f"{NEXUS_URL_RAW}?t={st.session_state.get('refresh_count', 0)}")
        
        if response.status_code == 200:
            log_content = response.text
            st.code(log_content, language="json") # 또는 text, yaml 등 로그 형식에 맞춰 변경
            st.caption(f"📍 Target: {NEXUS_URL_RAW}")
        else:
            st.warning("⚠️ Nexus 신호가 미약합니다. (Gist 연결 실패)")
            
    except Exception as e:
        st.error(f"❌ 통신 오류 발생: {e}")

# ------------------------------------------
# TAB 2: COMMAND CENTER (지시 하달)
# ------------------------------------------
with tab2:
    st.subheader("💬 Command Interface")

    # 대화 기록 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 이전 대화 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["parts"][0]["text"])

    # 사용자 입력 대기
    if prompt := st.chat_input("CEO님의 명령을 입력하십시오..."):
        # 1. 사용자 메시지 표시
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "parts": [{"text": prompt}]})

        # 2. AI 응답 생성 (여기에 '관제관 페르소나'가 적용됨)
        with st.chat_message("assistant"):
            with st.spinner(f"Thinking with {model_option}..."):
                # modules/gemini_brain.py의 get_response 함수 호출
                response_text = brain.get_response(st.session_state.messages, prompt, model_name=model_option)
                st.markdown(response_text)
        
        # 3. AI 응답 저장
        st.session_state.messages.append({"role": "model", "parts": [{"text": response_text}]})
