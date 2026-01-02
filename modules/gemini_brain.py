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
            system_instruction="당신은 사용자의 요청을 수행하는 유능하고 충실한 AI 비서입니다. 항상 '하십시오'체의 격식 있고 정중한 존댓말을 사용하세요. 답변은 명확하고 간결하게 작성하세요."
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
