# 즉시 배포 가이드 🚀

## 현재 상태
- ✅ 로컬 파일 수정 완료
- ❌ GitHub에 푸시 필요
- ❌ Streamlit Cloud 배포 대기 중

## 배포 단계

### 1단계: Git 커밋 및 푸시

#### Windows (PowerShell 또는 Git Bash)
```bash
cd multi-channel-agent

# 변경사항 확인
git status

# 모든 변경사항 스테이징
git add .

# 커밋 (한글 메시지)
git commit -m "UI 레이아웃 복구 및 콘텐츠 생성 품질 개선"

# GitHub에 푸시
git push origin main
```

또는 **GitHub Desktop 사용**:
1. GitHub Desktop 열기
2. 변경된 파일 확인
3. 커밋 메시지 입력: "UI 레이아웃 복구 및 콘텐츠 생성 품질 개선"
4. "Commit to main" 클릭
5. "Push origin" 클릭

### 2단계: Streamlit Cloud 자동 배포 확인

1. **Streamlit Cloud 대시보드 접속**
   - https://share.streamlit.io/
   - 로그인

2. **앱 선택**
   - 배포된 앱 클릭

3. **배포 상태 확인**
   - "Manage app" 클릭
   - "Logs" 탭에서 진행 상황 확인
   - "Building..." → "Running" 상태 확인

4. **배포 완료 대기**
   - 보통 3-5분 소요
   - 완료되면 자동으로 새 버전 적용

### 3단계: 배포 확인

1. **앱 URL 접속**
   - 배포된 앱 URL 접속
   - 예: https://your-app-name.streamlit.app

2. **UI 확인**
   - [ ] 좌우 레이아웃이 1:1.2 비율인가?
   - [ ] 좌측에 입력 폼이 잘 보이는가?
   - [ ] 우측에 결과 탭이 잘 보이는가?

3. **기능 테스트**
   - [ ] 콘텐츠 생성이 작동하는가?
   - [ ] 생성된 콘텐츠가 500자 이상인가?
   - [ ] 마크다운 미리보기가 작동하는가?

## 문제 해결

### 문제 1: git push 실패

**오류**: `Permission denied` 또는 `Authentication failed`

**해결**:
```bash
# GitHub 인증 확인
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Personal Access Token 사용
# GitHub → Settings → Developer settings → Personal access tokens
# 토큰 생성 후 비밀번호 대신 사용
```

### 문제 2: Streamlit Cloud 빌드 실패

**원인**: 의존성 문제 또는 코드 오류

**해결**:
1. Streamlit Cloud Logs 확인
2. 오류 메시지 확인
3. 필요시 `requirements.txt` 확인:
   ```
   streamlit>=1.28.0
   google-generativeai>=0.8.3
   python-dotenv>=1.0.0
   ```

### 문제 3: GEMINI_API_KEY 오류

**원인**: Streamlit Cloud Secrets 미설정

**해결**:
1. Streamlit Cloud 대시보드 → 앱 선택
2. "Settings" → "Secrets" 클릭
3. 다음 내용 추가:
   ```toml
   GEMINI_API_KEY = "AIza..."
   ```
4. "Save" 클릭
5. 앱 자동 재시작 대기

## 배포 체크리스트

### 배포 전
- [x] 로컬에서 테스트 완료
- [ ] Git 커밋 및 푸시
- [ ] GitHub에서 변경사항 확인

### 배포 중
- [ ] Streamlit Cloud에서 빌드 시작 확인
- [ ] Logs에서 오류 없는지 확인
- [ ] "Running" 상태 확인

### 배포 후
- [ ] 앱 URL 접속 확인
- [ ] UI 레이아웃 확인
- [ ] 콘텐츠 생성 테스트
- [ ] 품질 확인 (500자 이상)

## 예상 소요 시간

| 단계 | 소요 시간 |
|------|----------|
| Git 커밋 및 푸시 | 1-2분 |
| Streamlit Cloud 감지 | 1-2분 |
| 빌드 및 배포 | 3-5분 |
| **총 소요 시간** | **5-10분** |

## 배포 후 확인 사항

### 1. UI 레이아웃
```
✅ 좌측 (1) : 우측 (1.2) 비율
✅ 입력 폼이 좌측에 배치
✅ 결과 탭이 우측에 배치
```

### 2. 콘텐츠 품질
```
✅ 블로그 1,500자 이상
✅ LinkedIn 800자 이상
✅ Twitter 각 트윗 200자 이상
✅ 이메일 500자 이상
```

### 3. 새로운 기능
```
✅ 마크다운 미리보기 토글
✅ 텍스트 영역 높이 500px
✅ Thinking Process 표시
✅ 섹션 헤더 (📌 제목, 📄 본문)
```

## 빠른 명령어 (복사해서 사용)

### Git 푸시 (한 번에)
```bash
cd multi-channel-agent && git add . && git commit -m "UI 레이아웃 복구 및 콘텐츠 생성 품질 개선" && git push origin main
```

### 배포 상태 확인 URL
```
https://share.streamlit.io/
```

## 도움말

### GitHub Desktop 사용 (추천)
1. 더 쉬운 GUI 인터페이스
2. 변경사항 시각적 확인
3. 충돌 해결 도구 제공

**다운로드**: https://desktop.github.com/

### 명령줄 사용
```bash
# 현재 브랜치 확인
git branch

# 원격 저장소 확인
git remote -v

# 최근 커밋 확인
git log --oneline -5

# 변경사항 확인
git diff
```

## 다음 단계

배포가 완료되면:
1. ✅ 앱 URL 접속하여 테스트
2. ✅ 실제 콘텐츠 생성 테스트
3. ✅ 품질 확인
4. ✅ 필요시 추가 개선

---

**중요**: 배포 전에 로컬에서 한 번 더 테스트하는 것을 권장합니다!

```bash
cd multi-channel-agent
streamlit run app.py
```
