import time
import requests
import toml
import os
import sys

# 모듈 경로 추가 (현재 스크립트가 root에 있으므로 modules 패키지 인식 가능)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules import gemini_brain
from modules import nexus_bridge

# ==========================================
# [CONFIGURATION]
# ==========================================
SECRETS_PATH = ".streamlit/secrets.toml"
NEXUS_URL_RAW = "https://gist.githubusercontent.com/MarlonHwang/c623d6f42e9e2867c6ac273a813a5392/raw/AURA_NEXUS.md"

def load_secrets():
    try:
        with open(SECRETS_PATH, "r", encoding="utf-8") as f:
            return toml.load(f)
    except Exception as e:
        print(f"❌ Critical Error: Secrets 로드 실패 - {e}")
        return None

# ==========================================
# [CORE LOGIC]
# ==========================================
def run_neural_link():
    print("🔌 Neural Link Receiver: Initializing...")
    
    # 1. 환경 설정 로드
    secrets = load_secrets()
    if not secrets:
        return

    TELEGRAM_TOKEN = secrets["telegram"]["bot_token"]
    CEO_CHAT_ID = str(secrets["telegram"]["chat_id"]) # 문자열로 비교
    GEMINI_API_KEY = secrets["gemini"]["api_key"]

    # 2. Brain 초기화
    # gemini_brain.init_gemini()는 st.secrets를 쓰므로, 여기서는 직접 configure 해야 함
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        print("🧠 Gemini Brain: Connected")
    except Exception as e:
        print(f"❌ Brain Connection Failed: {e}")
        return

    # 3. Telegram Polling Loop
    offset = 0
    print("📡 Neural Link: Online & Listening...")
    print(f"   (Target CEO ID: ...{CEO_CHAT_ID[-4:]})")

    while True:
        try:
            # Long Polling (30초 대기)
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
            params = {"offset": offset + 1, "timeout": 30}
            
            response = requests.get(url, params=params)
            data = response.json()

            if "result" in data:
                for update in data["result"]:
                    update_id = update["update_id"]
                    offset = update_id # 오프셋 갱신

                    # 메시지 처리
                    if "message" in update:
                        msg = update["message"]
                        sender_id = str(msg.get("chat", {}).get("id"))
                        text = msg.get("text", "")

                        # 보안 검사: CEO인지 확인
                        if sender_id != CEO_CHAT_ID:
                            print(f"⚠️ Unauthorized Access Detected from {sender_id}")
                            continue

                        print(f"📩 CEO Message: {text}")

                        # 1) "수신 중..." 표시 (Typing Action)
                        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendChatAction", 
                                      json={"chat_id": CEO_CHAT_ID, "action": "typing"})

                        # 2) Nexus 로그 확보 (상황 인식)
                        nexus_log = nexus_bridge.get_nexus_log(NEXUS_URL_RAW)
                        
                        # 3) Gemini에게 전달 (Trio 회의)
                        # Nexus context를 포함하여 질문
                        # get_response(history, user_input, model_name, nexus_context) 이므로 history=[] 전달
                        ai_response = gemini_brain.get_response([], text, nexus_context=nexus_log)

                        # 4) 답변 전송
                        print(f"🤖 Brain Reply: {ai_response[:30]}...")
                        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                                      json={"chat_id": CEO_CHAT_ID, "text": ai_response})

        except Exception as e:
            print(f"⚠️ Link Error: {e}")
            time.sleep(5) # 에러 발생 시 잠시 대기

        time.sleep(1) # CPU 과부하 방지

if __name__ == "__main__":
    run_neural_link()
