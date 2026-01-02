import requests
import json
import toml

# 1. Load Secrets
try:
    with open(".streamlit/secrets.toml", "r", encoding="utf-8") as f:
        secrets = toml.load(f)
    TOKEN = secrets["github"]["token"]
except Exception as e:
    print(f"❌ Error loading secrets: {e}")
    exit()

# 2. Read Nexus Content
try:
    with open("AURA_NEXUS.md", "r", encoding="utf-8") as f:
        content = f.read()
except Exception as e:
    print(f"❌ Error reading AURA_NEXUS.md: {e}")
    exit()

# 3. Create Gist
url = "https://api.github.com/gists"
headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
payload = {
    "description": "🗼 AURA NEXUS: Project Trinity (Lighthouse Log)",
    "public": False,  # Secret Gist
    "files": {
        "AURA_NEXUS.md": {
            "content": content
        }
    }
}

print("🚀 Uploading to Gist...")
response = requests.post(url, headers=headers, json=payload)

if response.status_code == 201:
    data = response.json()
    gist_id = data["id"]
    raw_url = data["files"]["AURA_NEXUS.md"]["raw_url"]
    html_url = data["html_url"]
    
    print(f"✅ SUCCESS!")
    print(f"🆔 GIST_ID: {gist_id}")
    print(f"🔗 RAW_URL: {raw_url}")
    print(f"🌐 VIEW_URL: {html_url}")
else:
    print(f"❌ Failed: {response.status_code}")
    print(response.text)
