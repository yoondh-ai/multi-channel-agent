# 🚀 Streamlit Cloud 배포 가이드

## 1단계: GitHub에 코드 업로드

### Git 초기화 및 푸시
```bash
# Git 초기화
git init

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit: Multi-channel posting agent"

# GitHub 저장소 생성 후 연결
git remote add origin https://github.com/[your-username]/[repo-name].git

# 푸시
git branch -M main
git push -u origin main
```

## 2단계: Streamlit Cloud 배포

1. **Streamlit Cloud 접속**
   - https://streamlit.io/cloud 방문
   - GitHub 계정으로 로그인

2. **New app 클릭**
   - Repository 선택
   - Branch: `main`
   - Main file path: `app.py`

3. **Advanced settings 클릭**
   - Secrets 섹션에 API 키 입력:
   ```toml
   OPENAI_API_KEY = "your-openai-api-key"
   TWITTER_API_KEY = "your-twitter-key"
   TWITTER_API_SECRET = "your-twitter-secret"
   TWITTER_ACCESS_TOKEN = "your-access-token"
   TWITTER_ACCESS_TOKEN_SECRET = "your-access-token-secret"
   MEDIUM_ACCESS_TOKEN = "your-medium-token"
   ```

4. **Deploy! 클릭**
   - 2-3분 후 자동으로 배포 완료
   - 공개 URL 생성됨 (예: https://your-app.streamlit.app)

## 3단계: 공유

생성된 URL을 해커톤 심사위원이나 팀원들과 공유하세요!

## 문제 해결

### 배포 실패 시
- `requirements.txt` 확인
- Python 버전 호환성 확인 (Python 3.9-3.11 권장)
- Streamlit Cloud 로그 확인

### API 키 오류 시
- Secrets 설정 재확인
- 앱 재시작 (Streamlit Cloud에서 Reboot 클릭)

## 로컬 테스트

배포 전 로컬에서 테스트:
```bash
streamlit run app.py
```

## 업데이트

코드 수정 후:
```bash
git add .
git commit -m "Update features"
git push
```

Streamlit Cloud가 자동으로 재배포합니다!
