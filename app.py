import streamlit as st
import requests
import modules.gemini_brain as brain

# ==========================================
# [CONFIG] 시스템 설정 및 좌표
# ==========================================
# CEO가 하달한 Nexus(Gist) 접선 장소 -> [변경] GitHub Lighthouse (AURA_NEXUS.md)
NEXUS_URL_RAW = "https://gist.githubusercontent.com/MarlonHwang/c623d6f42e9e2867c6ac273a813a5392/raw/AURA_NEXUS.md"

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
            "gemini-2.5-flash",          # [CEO Pick] 현재 지원되는 안정적인 모델
            "gemini-3-flash",            # [옵션] 고성능 (Quota 주의)
        ),
        index=0
    )
    st.caption(f"🚀 System Version: v6.0 (Silent Nexus)")
    st.toast("🤫 Nexus Log: Silent Mode Active")
    
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
# [HELPER] Nexus 통신 모듈
# ==========================================
def fetch_nexus_log():
    try:
        # [Cache Buster] Gist CDN 캐시를 뚫기 위해 무작위 타임스탬프 추가
        import time
        response = requests.get(f"{NEXUS_URL_RAW}?v={str(time.time())}")
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception:
        return None

# ==========================================
# [HELPER] Telegram 경보 발송
# ==========================================
def send_telegram_alert(message):
    try:
        if "telegram" in st.secrets:
            token = st.secrets["telegram"]["bot_token"]
            chat_id = st.secrets["telegram"]["chat_id"]
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {"chat_id": chat_id, "text": message}
            requests.post(url, json=payload)
    except Exception:
        pass # 조용히 실패

# ==========================================
# [MAIN] 탭 레이아웃 (Monitor & Command)
# ==========================================
tab1, tab2 = st.tabs(["📡 MONITOR (Nexus)", "💬 COMMAND (Gemini)"])

# ------------------------------------------
# TAB 1: NEXUS MONITOR (상황 관제)
# ------------------------------------------
with tab1:
    st.subheader("📡 Real-time Operation Log")
    
    log_content = fetch_nexus_log()
    
    if log_content:
        # [Visual] Markdown 렌더링
        st.markdown(log_content)
        st.caption(f"📍 Source: Nexus Gist (Live)")
        
        # [ALERT] 긴급 호출 코드 감지
        if "[CALL CEO]" in log_content:
            st.error("🚨 EMERGENCY CALL DETECTED! (Sending Alert...)")
            # 세션에 기록해서 중복 발송 방지 (간이 로직)
            if not st.session_state.get("alert_sent", False):
                send_telegram_alert("🚨 [TRINITY ALERT]\nNexus에서 긴급 호출 신호가 감지되었습니다!\n즉시 상황판을 확인하십시오.")
                st.session_state["alert_sent"] = True
                st.toast("🚨 Telegram Alert Sent!")
    else:
        st.warning("⚠️ Nexus 신호가 미약합니다. (GitHub 연결 실패)")

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
            # [Nexus Vision] 답변 직전에 몰래 로그를 훔쳐옴
            current_nexus_context = fetch_nexus_log()
            
            with st.spinner(f"Thinking with {model_option} + Nexus Vision..."):
                # modules/gemini_brain.py의 get_response 함수 호출 (nexus_context 전달)
                response_text = brain.get_response(
                    history=st.session_state.messages, 
                    user_input=prompt, 
                    model_name=model_option,
                    nexus_context=current_nexus_context  # <--- 핵심: 시력 공급
                )
                st.markdown(response_text)
        
        # 3. AI 응답 저장
        st.session_state.messages.append({"role": "model", "parts": [{"text": response_text}]})
