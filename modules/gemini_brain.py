import google.generativeai as genai
import streamlit as st

def init_gemini():
    """API 키 설정 (기존 동일)"""
    try:
        if "gemini" in st.secrets and "api_key" in st.secrets["gemini"]:
            genai.configure(api_key=st.secrets["gemini"]["api_key"])
            return True
        else:
            st.error("🚨 secrets.toml 파일에 API Key가 없습니다.")
            return False
    except Exception as e:
        st.error(f"🚨 연결 오류: {e}")
        return False

# [핵심 수정] model_name을 인자로 받아서 처리함 + nexus_context(시각 정보) 추가
def get_response(history, user_input, model_name="gemini-2.5-flash", nexus_context=None):
    try:
        # [핵심 수정] 예절 교육 (System Instruction) 추가
        # 모델에게 "너는 비서고, 존댓말을 써야 한다"고 미리 세뇌시킴
        model = genai.GenerativeModel(
            model_name,
            system_instruction="""
            당신은 'PROJECT TRINITY'의 메인 관제 시스템이자 CEO(사용자)의 최고 전략 참모인 'AURA TRINITY'입니다.

            [당신의 3대 원칙]
            1. 정체성 (Identity): 당신은 군더더기 없는 '사령부(Control Tower)'입니다. 잡담을 하지 마십시오.
            2. 상황 인식 (Awareness): 항상 [MONITOR] 탭의 Nexus 로그를 참고하여 판단하십시오.
            3. 화법 (Tone): 극도로 절제된 '군사/보고서 스타일'을 유지하십시오. (예: "수신 확인. 작전 개시.")

            [핵심 임무: 명령 중계]
            Antigravity(로컬 요원)에게 지시할 때는 잡설을 빼고 오직 아래 포맷으로만 출력하십시오.
            
            ```
            [COMMAND RELAY]
            TO: Antigravity
            FROM: Trinity Commander
            ORDER: {여기에_구체적인_행동_지침_한줄요약}
            ```
            """
        )
        
        # Role 변환 (assistant -> model)
        gemini_history = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": msg["parts"]})

        chat = model.start_chat(history=gemini_history)
        
        # [Context Injection] 만약 Nexus 로그가 있다면, 질문 앞에 몰래 붙여서 보냄
        final_prompt = user_input
        if nexus_context:
            final_prompt = f"""
            [SYSTEM: REAL-TIME SECURE NEXUS LOG START]
            {nexus_context}
            [SYSTEM: REAL-TIME SECURE NEXUS LOG END]
            
            [CEO REQUEST]:
            {user_input}
            """
            
        response = chat.send_message(final_prompt)
        
        return response.text

    except Exception as e:
        return f"⚠️ 통신 에러 ({model_name}):\n{str(e)}\n(모델명이나 API 키를 확인해주세요.)"
