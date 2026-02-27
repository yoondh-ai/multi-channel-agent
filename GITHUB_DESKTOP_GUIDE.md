# 🖥️ GitHub Desktop 업로드 가이드

## 1단계: GitHub Desktop 설치

1. **다운로드**
   - https://desktop.github.com/ 접속
   - "Download for Windows" 클릭
   - 다운로드 완료 후 실행

2. **설치**
   - 자동으로 설치 진행
   - 완료되면 GitHub Desktop 자동 실행

## 2단계: GitHub 계정 연결

1. **로그인**
   - "Sign in to GitHub.com" 클릭
   - 브라우저가 열리면 GitHub 계정으로 로그인
   - "Authorize desktop" 클릭
   - GitHub Desktop으로 자동 복귀

2. **Git 설정**
   - Name과 Email 입력 (자동으로 채워져 있을 수 있음)
   - "Finish" 클릭

## 3단계: 프로젝트 추가

1. **로컬 저장소 추가**
   - 메인 화면에서 "Add an Existing Repository from your Hard Drive" 클릭
   - 또는 메뉴: `File` → `Add local repository...`

2. **폴더 선택**
   - "Choose..." 버튼 클릭
   - 다음 경로로 이동:
     ```
     C:\Users\user\Desktop\AI 해커톤\kiro_test\multi-channel-agent
     ```
   - 폴더 선택 후 "폴더 선택" 클릭

3. **저장소 생성**
   - "The directory does not appear to be a Git repository" 메시지가 나타남
   - 파란색 "create a repository" 링크 클릭
   - Repository name: `multi-channel-agent` (자동 입력됨)
   - Description: `AI-powered multi-channel posting agent` (선택사항)
   - **중요: "Initialize this repository with a README" 체크 해제**
   - Git ignore: None
   - License: None
   - "Create Repository" 클릭

## 4단계: 첫 커밋

1. **변경사항 확인**
   - 왼쪽에 모든 파일 목록이 체크된 상태로 표시됨
   - 오른쪽에서 파일 내용 미리보기 가능

2. **커밋 메시지 작성**
   - 왼쪽 하단 "Summary" 입력란에:
     ```
     Initial commit: Multi-channel posting agent
     ```
   - Description은 비워둬도 됨

3. **커밋 실행**
   - 파란색 "Commit to main" 버튼 클릭
   - 완료되면 "No local changes" 메시지 표시

## 5단계: GitHub에 업로드 (Publish)

1. **Publish Repository**
   - 상단 중앙의 "Publish repository" 버튼 클릭
   - 팝업 창이 열림

2. **설정 확인**
   - Name: `multi-channel-agent`
   - Description: 자동 입력됨
   - **중요: "Keep this code private" 체크 해제** (Public으로 설정)
   - Organization: None (개인 계정)

3. **업로드**
   - "Publish Repository" 버튼 클릭
   - 업로드 진행 (몇 초 소요)
   - 완료!

## 6단계: 확인

1. **GitHub에서 확인**
   - GitHub Desktop 상단 메뉴: `Repository` → `View on GitHub`
   - 브라우저에서 저장소 페이지 열림
   - 모든 파일이 업로드된 것 확인

2. **저장소 URL 복사**
   - 주소창의 URL 복사 (나중에 Streamlit Cloud에서 사용)
   - 예: `https://github.com/your-username/multi-channel-agent`

---

## 다음 단계: Streamlit Cloud 배포

GitHub 업로드 완료! 이제 웹사이트로 배포하세요:

1. https://streamlit.io/cloud 접속
2. GitHub 계정으로 로그인
3. "New app" 클릭
4. 방금 만든 저장소 선택
5. Main file: `app.py`
6. Advanced settings → Secrets에 API 키 입력:
   ```toml
   OPENAI_API_KEY = "your-key-here"
   ```
7. "Deploy!" 클릭
8. 2-3분 후 공개 URL 생성!

---

## 코드 수정 후 업데이트 방법

1. 코드 수정 후 저장
2. GitHub Desktop 자동으로 변경사항 감지
3. 왼쪽 하단에 커밋 메시지 입력
4. "Commit to main" 클릭
5. 상단 "Push origin" 버튼 클릭
6. Streamlit Cloud가 자동으로 재배포!

---

## 문제 해결

### "Authentication failed"
- GitHub Desktop에서 로그아웃 후 재로그인
- `File` → `Options` → `Accounts` → `Sign out`

### 파일이 보이지 않음
- .gitignore 파일 확인
- .env 파일은 의도적으로 제외됨 (보안상 올리면 안 됨)

### Push 실패
- 인터넷 연결 확인
- GitHub 계정 상태 확인
