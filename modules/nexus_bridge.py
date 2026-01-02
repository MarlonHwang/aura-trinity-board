import requests
import streamlit as st

def get_nexus_log(gist_url):
    """지정된 Gist URL(Raw)에서 로그 데이터를 가져옵니다."""
    if not gist_url:
        return "Waiting for Nexus Link..."

    try:
        response = requests.get(gist_url)
        if response.status_code == 200:
            return response.text
        else:
            return f"❌ 데이터를 불러올 수 없습니다. (Status: {response.status_code})"
    except Exception as e:
        return f"⚠️ 네트워크 오류: {e}"
