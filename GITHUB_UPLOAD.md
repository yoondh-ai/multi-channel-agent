# 📤 GitHub 업로드 완벽 가이드

## 사전 준비

### 1. Git 설치 확인
```bash
git --version
```

Git이 없다면:
- Windows: https://git-scm.com/download/win 에서 다운로드
- 설치 시 모든 옵션 기본값으로 진행

### 2. GitHub 계정 생성
- https://github.com 접속
- Sign up 클릭
- 이메일, 비밀번호 입력하여 계정 생성

---

## 업로드 절차

### Step 1: GitHub에서 새 저장소 만들기

1. GitHub 로그인
2. 오른쪽 상단 `+` 버튼 클릭 → `New repository` 선택
3. 저장소 정보 입력:
   - Repository name: `multi-channel-agent` (원하는 이름)
   - Description: `AI-powered multi-channel posting agent`
   - Public 선택 (Streamlit Cloud 무료 배포용)
   - **중요: 아무것도 체크하지 마세요** (README, .gitignore 등)
4. `Create repository` 클릭

### Step 2: 로컬에서 Git 초기화

터미널(PowerShell)을 열고:

```bash
# 프로젝트 폴더로 이동
cd "C:\Users\user\Desktop\AI 해커톤\kiro_test\multi-channel-agent"

# Git 초기화
git init

# 사용자 정보 설정 (최초 1회만)
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit: Multi-channel posting agent"
```

### Step 3: GitHub에 연결 및 푸시

GitHub 저장소 페이지에 표시된 URL을 복사한 후:

```bash
# GitHub 저장소 연결 (URL은 본인 것으로 변경)
git remote add origin https://github.com/[your-username]/multi-channel-agent.git

# 브랜치 이름 변경
git branch -M main

# 푸시 (업로드)
git push -u origin main
```

### Step 4: GitHub 인증

푸시 시 인증 요구되면:

**방법 A - Personal Access Token (추천)**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. `Generate new token (classic)` 클릭
3. Note: `streamlit-deploy`
4. Expiration: `90 days`
5. 권한: `repo` 전체 체크
6. `Generate token` 클릭
7. 생성된 토큰 복사 (한 번만 보임!)
8. 터미널에서 비밀번호 대신 토큰 입력

**방법 B - GitHub Desktop (GUI)**
1. https://desktop.github.com/ 에서 다운로드
2. GitHub 로그인
3. `Add` → `Add existing repository` 선택
4. 프로젝트 폴더 선택
5. `Publish repository` 클릭

---

## 확인

GitHub 저장소 페이지를 새로고침하면 파일들이 업로드된 것을 확인할 수 있습니다!

---

## 문제 해결

### "git: command not found"
→ Git 설치 필요: https://git-scm.com/download/win

### "Permission denied"
→ Personal Access Token 사용 (위 방법 A 참고)

### "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/[your-username]/[repo-name].git
```

### 한글 경로 문제
```bash
git config --global core.quotepath false
```

---

## 다음 단계

업로드 완료 후 → `DEPLOY.md` 파일 참고하여 Streamlit Cloud 배포!
