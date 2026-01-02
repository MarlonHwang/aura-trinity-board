import os

# 생성할 디렉토리 목록
directories = [
    ".streamlit",
    "modules",
    "assets"
]

# 생성할 파일 목록 (빈 파일)
files = [
    ".streamlit/secrets.toml",   # 보안 금고
    "modules/__init__.py",       # 패키지 인식용
    "modules/gemini_brain.py",   # AI 두뇌 모듈
    "modules/nexus_bridge.py",   # 통신 모듈
    "modules/ui_components.py",  # 화면 디자인 모듈
    "app.py",                    # 메인 실행 파일
    "requirements.txt"           # 라이브러리 목록
]

def create_structure():
    print("🚀 구조 생성을 시작합니다...")
    
    # 1. 디렉토리 생성
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📂 폴더 생성: {directory}")
        else:
            print(f"✅ 폴더 존재: {directory}")

    # 2. 파일 생성
    for file in files:
        if not os.path.exists(file):
            with open(file, 'w', encoding='utf-8') as f:
                pass # 빈 파일 생성
            print(f"📄 파일 생성: {file}")
        else:
            print(f"✅ 파일 존재: {file}")
            
    print("✨ 모든 골조 공사가 완료되었습니다.")

if __name__ == "__main__":
    create_structure()
