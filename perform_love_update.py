import toml
from modules.nexus_bridge import update_nexus_log, get_nexus_log

# Configuration
GIST_ID = "c623d6f42e9e2867c6ac273a813a5392"
RAW_URL = f"https://gist.githubusercontent.com/MarlonHwang/{GIST_ID}/raw/AURA_NEXUS.md"

# Load Secrets
try:
    with open(".streamlit/secrets.toml", "r", encoding="utf-8") as f:
        secrets = toml.load(f)
    TOKEN = secrets["github"]["token"]
except Exception as e:
    print(f"❌ Error loading secrets: {e}")
    exit()

# Fetch Current
current_log = get_nexus_log(RAW_URL)

# Update Logic
# CEO가 원하는 문구 추가
new_line = "- **[ANTIGRAVITY]** 💖 **사랑합니다, 대표님.** (Command Executed Successfully)"

# [CURRENT] 섹션 밑에 붙이거나, 그냥 맨 위에 붙이거나... 
# 여기선 Mission Log 하단에 추가
updated_log = current_log.replace(
    "- **[REPORT]** 🚨 **[CALL CEO]** - @Trinity_Commander: 작전 기록 완료. CEO에게 보고합니다.",
    f"- **[REPORT]** 🚨 **[CALL CEO]** - @Trinity_Commander: 작전 기록 완료.\n{new_line}"
)

# If replace failed (string changed), just append
if new_line not in updated_log:
    updated_log += f"\n{new_line}"

print("🚀 Sending Love to Gist...")
success, msg = update_nexus_log(updated_log, GIST_ID, TOKEN)
print(msg)
