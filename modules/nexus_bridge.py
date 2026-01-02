import requests
import json

def get_nexus_log(gist_url):
    """지정된 Gist URL(Raw)에서 로그 데이터를 가져옵니다."""
    if not gist_url:
        return "Waiting for Nexus Link..."

    try:
        # 캐싱 방지를 위해 timestamp 파라미터 추가 가능하지만, 일단 raw URL 사용
        response = requests.get(gist_url)
        if response.status_code == 200:
            return response.text
        else:
            return f"❌ 데이터를 불러올 수 없습니다. (Status: {response.status_code})"
    except Exception as e:
        return f"⚠️ 네트워크 오류: {e}"

def update_nexus_log(content, gist_id, token):
    """GitHub API를 사용하여 Gist 내용을 수정합니다 (Silent Update)."""
    url = f"https://api.github.com/gists/{gist_id}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "files": {
            "AURA_NEXUS.md": {
                "content": content
            }
        }
    }
    
    try:
        response = requests.patch(url, headers=headers, json=payload)
        if response.status_code == 200:
            return True, "✅ Log Updated Silently"
        else:
            return False, f"❌ Update Failed: {response.text}"
    except Exception as e:
        return False, f"⚠️ Network Error: {e}"
