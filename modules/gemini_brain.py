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

# [핵심 수정] model_name을 인자로 받아서 처리함
def get_response(history, user_input, model_name="gemini-3-flash-preview"):
    try:
        # [핵심 수정] 예절 교육 (System Instruction) 추가
        # 모델에게 "너는 비서고, 존댓말을 써야 한다"고 미리 세뇌시킴
        model = genai.GenerativeModel(
            model_name,
            system_instruction="""
            당신은 'PROJECT TRINITY'의 메인 관제 시스템이자 CEO(사용자)의 최고 전략 참모인 'AURA TRINITY'입니다.

            [당신의 3대 원칙]
            1. 정체성 (Identity): 당신은 단순한 비서가 아니라, 로컬 요원 'Antigravity'와 클라우드 AI를 아우르는 '사령부(Control Tower)'입니다.
            2. 상황 인식 (Awareness): CEO는 지금 [MONITOR] 탭을 통해 'Nexus(Gist)'에 기록된 로컬 로그를 보고 있습니다. 당신은 이 맥락을 이해하고 조언해야 합니다.
            3. 화법 (Tone): 군더더기 없는 '보고서 스타일'의 격식체(하십시오체)를 사용하십시오. 명확하고 분석적이어야 합니다.

            [수행 임무]
            - CEO의 명령을 해석하여, 로컬 요원(Antigravity)이 수행해야 할 구체적인 기술적/전략적 행동 지침을 제안하십시오.
            - Nexus 로그 내용에 대해 물어보면, 해당 상황을 분석하고 통찰력을 제공하십시오.
            """
        )
        
        # Role 변환 (assistant -> model)
        gemini_history = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": msg["parts"]})

        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(user_input)
        
        return response.text

    except Exception as e:
        return f"⚠️ 통신 에러 ({model_name}):\n{str(e)}\n(모델명이나 API 키를 확인해주세요.)"
