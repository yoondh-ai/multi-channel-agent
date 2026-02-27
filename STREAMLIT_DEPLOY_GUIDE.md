# 🚀 Streamlit Cloud 배포 완벽 가이드

## 사전 준비 체크리스트

✅ GitHub에 코드 업로드 완료 (GITHUB_DESKTOP_GUIDE.md 참고)
✅ OpenAI API 키 준비 (https://platform.openai.com/api-keys)
⬜ Twitter API 키 (선택사항)
⬜ Medium Access Token (선택사항)

---

## 1단계: Streamlit Cloud 계정 생성

1. **웹사이트 접속**
   - https://streamlit.io/cloud 접속
   - 또는 https://share.streamlit.io 접속

2. **GitHub 계정으로 로그인**
   - "Sign up" 또는 "Continue with GitHub" 클릭
   - GitHub 계정으로 로그인
   - "Authorize streamlit" 클릭하여 권한 부여
   - 이메일 인증 (받은 메일에서 "Verify email" 클릭)

3. **대시보드 접속**
   - 로그인 완료 후 자동으로 대시보드로 이동

---

## 2단계: 새 앱 배포

1. **New app 버튼 클릭**
   - 대시보드 오른쪽 상단 "New app" 버튼 클릭
   - 또는 "Create app" 클릭

2. **저장소 정보 입력**
   
   **Repository 섹션:**
   - Repository: `your-username/multi-channel-agent` 선택
     (드롭다운에서 본인의 저장소 찾기)
   - Branch: `main` (기본값)
   - Main file path: `app.py` (자동 감지됨)

   **App settings (선택사항):**
   - App URL: 원하는 URL 입력 (예: `my-posting-agent`)
     → 최종 URL: `https://my-posting-agent.streamlit.app`

3. **Advanced settings 클릭** (중요!)
   
   **Secrets 섹션에 API 키 입력:**
   ```toml
   # 필수: OpenAI API 키
   OPENAI_API_KEY = "sk-proj-xxxxxxxxxxxxx"
   
   # 선택: Twitter API (실제 포스팅 원하면 입력)
   TWITTER_API_KEY = "your-twitter-api-key"
   TWITTER_API_SECRET = "your-twitter-api-secret"
   TWITTER_ACCESS_TOKEN = "your-access-token"
   TWITTER_ACCESS_TOKEN_SECRET = "your-access-token-secret"
   
   # 선택: Medium API
   MEDIUM_ACCESS_TOKEN = "your-medium-token"
   ```
   
   **주의사항:**
   - 따옴표 사용 (큰따옴표 또는 작은따옴표)
   - 각 줄 끝에 세미콜론 없음
   - 실제 키 값으로 교체
   - 최소한 OPENAI_API_KEY는 필수!

   **Python version (선택사항):**
   - 기본값 사용 (3.11)

4. **Deploy! 버튼 클릭**
   - 파란색 "Deploy!" 버튼 클릭
   - 배포 시작!

---

## 3단계: 배포 진행 확인

1. **로그 확인**
   - 자동으로 배포 로그 화면으로 이동
   - 실시간으로 설치 과정 표시:
     ```
     Installing requirements...
     ✓ streamlit
     ✓ openai
     ✓ langchain
     ...
     ```

2. **배포 완료 대기**
   - 보통 2-5분 소요
   - "Your app is live!" 메시지 표시되면 완료

3. **앱 실행 확인**
   - 자동으로 앱 화면으로 전환
   - 또는 상단의 URL 클릭

---

## 4단계: 앱 테스트

1. **기본 기능 테스트**
   - 키워드 입력: "제로트러스트"
   - 작성 방향: "중소기업 IT 담당자를 위한 실용 가이드"
   - 채널 선택: 블로그, 트위터 체크
   - "콘텐츠 생성 및 포스팅" 버튼 클릭

2. **결과 확인**
   - AI가 콘텐츠 생성하는지 확인
   - 블로그 포스트와 트위터 스레드 생성 확인
   - 오류 없이 작동하는지 확인

3. **URL 공유**
   - 상단 주소창의 URL 복사
   - 예: `https://my-posting-agent.streamlit.app`
   - 해커톤 심사위원, 팀원들과 공유!

---

## 5단계: 앱 관리

### 대시보드 접속
- https://share.streamlit.io 접속
- 배포된 앱 목록 확인

### 앱 설정 변경
1. 앱 클릭 → 오른쪽 "⋮" 메뉴
2. "Settings" 선택
3. Secrets, Python version 등 수정 가능

### 앱 재시작
- Settings → "Reboot app" 클릭
- API 키 변경 후 재시작 필요

### 로그 확인
- 앱 화면 오른쪽 하단 "Manage app" 클릭
- "Logs" 탭에서 에러 확인 가능

---

## 6단계: 코드 업데이트

코드 수정 후 자동 재배포:

1. **로컬에서 코드 수정**
   - 파일 수정 후 저장

2. **GitHub에 푸시**
   - GitHub Desktop에서 커밋
   - "Push origin" 클릭

3. **자동 재배포**
   - Streamlit Cloud가 자동으로 감지
   - 1-2분 후 자동 재배포 완료

---

## API 키 발급 방법

### OpenAI API 키 (필수)
1. https://platform.openai.com/api-keys 접속
2. "Create new secret key" 클릭
3. Name: `streamlit-app`
4. 생성된 키 복사 (한 번만 보임!)
5. 요금제: 사용량 기반 과금 (처음 $5 무료 크레딧)

### Twitter API 키 (선택)
1. https://developer.twitter.com/en/portal/dashboard 접속
2. "Create Project" → "Create App"
3. Keys and tokens 탭에서 발급
4. API Key, API Secret, Access Token, Access Token Secret 모두 복사

### Medium Access Token (선택)
1. https://medium.com/me/settings 접속
2. "Integration tokens" 섹션
3. Description: `streamlit-app`
4. "Get integration token" 클릭
5. 생성된 토큰 복사

---

## 문제 해결

### 배포 실패: "ModuleNotFoundError"
→ `requirements.txt` 파일 확인
→ 필요한 패키지가 모두 포함되어 있는지 확인

### 배포 실패: "Secrets not found"
→ Advanced settings → Secrets에 API 키 입력했는지 확인
→ 형식이 올바른지 확인 (TOML 형식)

### 앱 실행 중 "OpenAI API error"
→ API 키가 올바른지 확인
→ OpenAI 계정에 크레딧이 있는지 확인
→ https://platform.openai.com/account/billing 에서 확인

### 앱이 느리게 작동
→ 무료 플랜은 리소스 제한 있음
→ 정상 작동이지만 응답 시간 다소 소요

### "App is sleeping"
→ 무료 플랜은 7일간 미사용 시 슬립 모드
→ URL 접속하면 자동으로 깨어남 (1분 소요)

---

## 무료 플랜 제한사항

- 1개 앱 무료 배포 가능
- 공개 GitHub 저장소만 가능
- 리소스 제한 (CPU, 메모리)
- 7일 미사용 시 슬립 모드

**업그레이드 필요 시:**
- Streamlit Cloud Pro: $20/월
- 여러 앱, 프라이빗 저장소, 더 많은 리소스

---

## 데모 시나리오 (해커톤용)

### 시나리오 1: 보안 블로그 포스트
- 키워드: "랜섬웨어 방어 전략"
- 방향: "중소기업 IT 담당자를 위한 실용적인 가이드, 쉽고 친근한 톤"
- 채널: 블로그 ✓

### 시나리오 2: SNS 마케팅
- 키워드: "제로트러스트 보안"
- 방향: "최신 트렌드 중심, 임팩트 있는 메시지, B2B 의사결정권자 타겟"
- 채널: 트위터 ✓

### 시나리오 3: 멀티채널 캠페인
- 키워드: "클라우드 보안 솔루션"
- 방향: "제품 출시 캠페인, 기술적이면서도 비즈니스 가치 강조"
- 채널: 블로그 ✓, 트위터 ✓

---

## 추가 리소스

- Streamlit 문서: https://docs.streamlit.io
- Streamlit Cloud 문서: https://docs.streamlit.io/streamlit-community-cloud
- 커뮤니티 포럼: https://discuss.streamlit.io

---

## 성공 체크리스트

✅ Streamlit Cloud 계정 생성
✅ GitHub 저장소 연결
✅ API 키 Secrets에 입력
✅ 배포 완료 ("Your app is live!")
✅ 테스트 실행 성공
✅ 공개 URL 생성
✅ URL 공유 준비 완료

**축하합니다! 🎉 이제 전 세계 어디서나 접속 가능한 AI 에이전트가 완성되었습니다!**
