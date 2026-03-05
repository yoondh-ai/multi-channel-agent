# 🎯 Gemini 1.5 Flash 설정 가이드

## ✨ 완전히 새로운 버전!

이 프로젝트는 **Gemini 1.5 Flash**로 완전히 업그레이드되었습니다!

### 주요 변경사항
- ✅ **Gemini 1.5 Flash 전용**: `google-generativeai` 라이브러리 사용
- ✅ **st.secrets 통합**: 보안을 위해 Streamlit Secrets 사용
- ✅ **브랜드 가이드라인 학습**: `.kiro/steering/` 문서를 system_instruction에 주입
- ✅ **Jasper 스타일 UI**: 좌우 분할 레이아웃
- ✅ **직접 수정 가능**: st.text_area로 결과물 편집
- ✅ **발행 기능**: 각 채널별 발행 버튼 추가

## 🚀 빠른 시작

### 1단계: Gemini API 키 발급 (무료, 30초)

1. **https://aistudio.google.com/app/apikey** 접속
2. Google 계정으로 로그인
3. **"Create API Key"** 버튼 클릭
4. 프로젝트 선택 또는 새로 생성
5. 생성된 API 키 복사 (`AIza`로 시작)

**무료 할당량:**
- 분당 15 요청
- 일일 1,500 요청
- 월 100만 토큰 무료

충분히 넉넉합니다! 🎉

### 2단계: Streamlit Cloud Secrets 설정

#### Streamlit Cloud에서:
1. 앱 대시보드 접속
2. 앱 선택 → **Settings** (⚙️) 클릭
3. **"Secrets"** 탭 선택
4. 다음 내용 추가:

```toml
GEMINI_API_KEY = "AIza여기에_복사한_키_붙여넣기"
```

5. **"Save"** 클릭
6. 앱 자동 재시작 대기 (약 30초)

#### 로컬 개발 환경에서:
`.streamlit/secrets.toml` 파일 생성:

```toml
GEMINI_API_KEY = "AIza여기에_복사한_키_붙여넣기"
```

### 3단계: 확인

앱 실행 후:
```
✅ Gemini 1.5 Flash (무료) 연결됨
```

메시지 확인!

## 📋 브랜드 가이드라인 설정

### 가이드라인 문서 위치
```
multi-channel-agent/
└── .kiro/
    └── steering/
        ├── brand_voice.md          # 브랜드 보이스
        └── content_guidelines.md   # 콘텐츠 작성 가이드
```

### 자동 로드
모든 `.kiro/steering/*.md` 파일이 자동으로:
1. 로드됨
2. Gemini의 `system_instruction`에 주입됨
3. AI가 브랜드 톤을 완벽히 학습

### 커스터마이징

#### 새 가이드라인 추가
`.kiro/steering/seo_guidelines.md` 파일 생성:

```markdown
# SEO 가이드라인

## 키워드 사용
- 자연스럽게 3-5회 반복
- 제목에 반드시 포함
- 첫 단락에 포함

## 메타 설명
- 150-160자
- 행동 유도 포함
```

자동으로 로드됩니다!

#### 기존 가이드라인 수정
`.kiro/steering/brand_voice.md` 편집:

```markdown
# 우리 회사 브랜드 보이스

## 브랜드 정체성
[회사 소개]

## 핵심 가치
- 가치 1
- 가치 2
```

## 🎨 UI/UX 특징

### Jasper 스타일 레이아웃

#### 좌측 (50%): 입력 폼
- 제품/서비스명
- 핵심 특징
- 타겟 키워드
- 추가 정보
- 타겟 독자
- 말투 (Tone)
- 마케팅 프레임워크
- 생성 옵션

#### 우측 (50%): 결과 및 편집
- 채널별 탭 (블로그, LinkedIn, Twitter, 이메일)
- 버전별 서브탭
- **직접 수정 가능한 텍스트 영역**
- Thinking Process 표시
- 메트릭 (글자 수, SEO, 가독성)
- 액션 버튼 (복사, 다운로드, 재생성)
- **발행 버튼**

### 직접 수정 기능

생성된 콘텐츠를 `st.text_area`에서 직접 수정 가능:
- 실시간 편집
- 자동 저장 (세션)
- 수정된 내용으로 발행

## 🚀 발행 기능

### 지원 채널
- 📝 네이버 블로그
- 💼 LinkedIn
- 🐦 Twitter
- 📧 이메일

### 발행 스크립트 위치
```
multi-channel-agent/
└── scripts/
    ├── __init__.py
    ├── publish_blog.py
    ├── publish_linkedin.py
    ├── publish_twitter.py
    └── publish_email.py
```

### 커스터마이징

#### 블로그 API 연동
`scripts/publish_blog.py` 편집:

```python
def publish_to_blog(title: str, content: str) -> dict:
    # TODO: 실제 API 연동
    # 예: Naver Blog API
    
    import requests
    
    response = requests.post(
        "https://api.blog.naver.com/...",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"title": title, "content": content}
    )
    
    return {
        "success": response.ok,
        "message": "발행 완료",
        "url": response.json()['url']
    }
```

#### LinkedIn API 연동
`scripts/publish_linkedin.py` 편집:

```python
def publish_to_linkedin(content: str) -> dict:
    # LinkedIn API v2 사용
    # https://docs.microsoft.com/en-us/linkedin/
    
    import requests
    
    response = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json={
            "author": f"urn:li:person:{PERSON_ID}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": content},
                    "shareMediaCategory": "NONE"
                }
            }
        }
    )
    
    return {
        "success": response.ok,
        "message": "발행 완료",
        "url": f"https://linkedin.com/posts/..."
    }
```

## 💡 사용 예시

### 1. 정보 입력
```
제품명: MarkAny 제로트러스트 솔루션
핵심 특징:
• 완벽한 보안 아키텍처
• 클라우드 네이티브 설계
• 실시간 위협 탐지
키워드: 제로트러스트, 클라우드 보안
타겟: IT 담당자
톤: 전문적
프레임워크: PAS
```

### 2. 생성 버튼 클릭
→ 4개 채널 × 2개 버전 = 8개 콘텐츠 생성

### 3. 결과 확인 및 수정
- 채널 탭 선택 (예: 네이버 블로그)
- 버전 선택 (예: 버전 1)
- Thinking Process 확인
- 텍스트 영역에서 직접 수정

### 4. 발행
- "📤 네이버 블로그에 발행" 버튼 클릭
- 발행 결과 확인

## 🔍 작동 원리

### System Instruction 구성
```python
system_instruction = f"""
당신은 MarkAny의 전문 마케팅 작성자입니다.

# 브랜드 가이드라인
{brand_voice.md 내용}
{content_guidelines.md 내용}
{기타 .md 파일 내용}

# 작성 원칙
- Thinking Process
- Data Grounding
- Full Paraphrasing
- 브랜드 톤 준수
"""
```

### User Prompt 구성
```python
user_prompt = f"""
# 소스 데이터 (최상단 배치)
제품명: {product_name}
핵심 특징: {key_features}
...

# 작성 요구사항
채널: {channel}
타겟: {audience}
톤: {tone}
...

# 작성 지시
1. Thinking Process 수행
2. 완전히 재작성
3. 데이터에만 기반
"""
```

### Gemini 호출
```python
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=system_instruction
)

response = model.generate_content(user_prompt)
```

## 💰 비용

### Gemini 1.5 Flash 무료 할당량
- **분당**: 15 요청
- **일일**: 1,500 요청
- **월간**: 100만 토큰

### 예상 사용량
- 블로그 포스트 1개: ~2,000 토큰
- 하루 10개 생성: ~20,000 토큰
- 월 300개: ~600,000 토큰

**완전 무료!** 🎉

### 유료 플랜 (필요시)
- $0.075 / 1M input tokens
- $0.30 / 1M output tokens

매우 저렴합니다!

## 🆚 비교

| 항목 | Gemini 1.5 Flash | AWS Bedrock | Groq |
|------|------------------|-------------|------|
| 비용 | ✅ 무료 (100만 토큰/월) | ❌ 유료 | ✅ 무료 |
| 설정 | ✅ API 키 1개 | ❌ IAM, 권한 등 | ✅ API 키 1개 |
| 브랜드 학습 | ✅ system_instruction | ✅ System Prompt | ⚠️ 제한적 |
| 한국어 | ✅ 우수 | 우수 | 우수 |
| 속도 | ✅ 빠름 | 보통 | 매우 빠름 |
| 안정성 | ✅ 높음 | 높음 | 보통 |
| 추천 | ⭐⭐⭐⭐⭐ | 프로덕션 | 테스트 |

## 🐛 문제 해결

### "GEMINI_API_KEY가 설정되지 않았습니다"
→ Streamlit Secrets 확인
→ `.streamlit/secrets.toml` 파일 확인
→ 앱 재시작

### "API 할당량 초과"
→ 무료 할당량 확인 (100만 토큰/월)
→ 유료 플랜 고려
→ 또는 다음 달까지 대기

### "JSON 파싱 실패"
→ 정상입니다 (가끔 발생)
→ 재생성 버튼 클릭
→ 원문이 표시됨

### 발행 실패
→ `scripts/` 폴더의 스크립트 확인
→ API 키 설정 확인
→ 로그 확인

## 📚 추가 리소스

- [Gemini API 문서](https://ai.google.dev/docs)
- [google-generativeai 라이브러리](https://github.com/google/generative-ai-python)
- [Streamlit Secrets](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)

## 🎉 결론

Gemini 1.5 Flash는:
- ✅ 완전 무료 (100만 토큰/월)
- ✅ 브랜드 가이드라인 완벽 학습
- ✅ Thinking Process 포함
- ✅ 직접 수정 가능
- ✅ 발행 기능 통합
- ✅ 설정 간단 (API 키 1개)

**해커톤에 완벽합니다!** 🚀

---

*마지막 업데이트: 2024년 3월*
