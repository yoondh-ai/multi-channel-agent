# ✨ AI 마케팅 콘텐츠 생성 플랫폼

보안 기술 문서를 고객의 마음을 사로잡는 마케팅 콘텐츠로 자동 변환하는 AI 에이전트

## 🎯 주요 기능

### 📝 다양한 콘텐츠 템플릿
- **블로그**: 포스트, 사례 연구, 백서
- **SNS**: Twitter 스레드, LinkedIn, Instagram, 카드뉴스
- **이메일**: 마케팅 이메일, 제품 런칭
- **광고**: Google Ads, 소셜 미디어 광고

### 🔍 실제 웹 리서치
- DuckDuckGo 자동 검색
- 최신 트렌드 분석
- 경쟁사 콘텐츠 분석

### 🎨 레퍼런스 학습
- 기존 콘텐츠 스타일 분석
- 톤앤매너 자동 학습
- 브랜드 일관성 유지

### ⚡ 빠른 생성
- 한 번에 최대 5개 버전 생성
- 실시간 편집 가능
- 다운로드 및 복사 지원

## 🚀 빠른 시작

### 1. API 키 발급 (30초, 완전 무료!)

**🎉 Groq 추천 (완전 무료, 가장 빠름)**

1. https://console.groq.com 접속
2. 이메일로 가입
3. API Keys → Create API Key
4. 생성된 키 복사

**왜 Groq인가?**
- ✅ 완전 무료 (신용카드 불필요)
- ✅ 초고속 (초당 500+ 토큰)
- ✅ Llama 3.1 70B 모델
- ✅ 안정적 (404 오류 없음)

자세한 가이드: [GROQ_SETUP_GUIDE.md](GROQ_SETUP_GUIDE.md)

### 2. 로컬 실행

```bash
# 저장소 클론
git clone <repository-url>
cd multi-channel-agent

# 패키지 설치
pip install -r requirements.txt

# 환경 변수 설정
echo "GROQ_API_KEY=gsk_your_key_here" > .env

# 앱 실행
streamlit run app.py
```

### 3. Streamlit Cloud 배포

1. GitHub에 푸시
2. https://streamlit.io/cloud 접속
3. "New app" → 저장소 선택
4. Settings → Secrets에 추가:
   ```toml
   GROQ_API_KEY = "gsk_your_key_here"
   ```
5. Deploy!

자세한 가이드: [STREAMLIT_DEPLOY_GUIDE.md](STREAMLIT_DEPLOY_GUIDE.md)

## 🔧 지원 LLM

| LLM | 상태 | 비용 | 속도 | 추천 |
|-----|------|------|------|------|
| **Groq** | ✅ 작동 | 무료 | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ |
| Gemini | ⚠️ 불안정 | 무료 (제한) | ⚡⚡ | ⭐⭐⭐ |
| OpenAI | ✅ 작동 | 유료 | ⚡⚡ | ⭐⭐⭐⭐ |

### 환경 변수 설정

```bash
# 옵션 1: Groq (추천)
GROQ_API_KEY=gsk_...

# 옵션 2: Gemini
GOOGLE_API_KEY=AIza...

# 옵션 3: OpenAI
OPENAI_API_KEY=sk-proj-...

# 선택사항: 고급 웹 검색
SERPER_API_KEY=...  # Google 검색 (2,500/월 무료)
TAVILY_API_KEY=...  # AI 검색 (1,000/월 무료)
```

## 📖 사용 방법

### 1. 템플릿 선택
- 카테고리 선택 (블로그, SNS, 이메일, 광고)
- 구체적인 템플릿 선택

### 2. 기본 정보 입력
- **키워드**: 핵심 주제 (예: "제로트러스트")
- **설명**: 구체적인 내용 (예: "중소기업을 위한 도입 가이드")

### 3. 타겟 설정
- **대상**: IT 관리자, CISO, 개발자 등
- **산업**: IT, 금융, 제조 등

### 4. 스타일 선택
- **톤**: 전문적, 친근한, 설득력 있는 등
- **길이**: 짧게 (<100자), 보통 (100-500자), 길게 (>500자)

### 5. 옵션 설정
- **생성 개수**: 1-5개 버전
- **CTA 포함**: 행동 유도 문구
- **SEO 최적화**: 검색 엔진 최적화

### 6. 레퍼런스 학습 (선택)
- 기존 콘텐츠 URL 입력
- AI가 스타일 자동 학습

### 7. 생성 및 편집
- "콘텐츠 생성" 클릭
- 실시간 편집 가능
- 버전별 비교

## 🎨 예시

### 입력
```
키워드: 제로트러스트
설명: 기업 보안을 위한 제로트러스트 아키텍처 도입 가이드
대상: IT 관리자
산업: 금융
톤: 전문적
길이: 길게
```

### 출력 (블로그 포스트)
```markdown
# 제로트러스트: 금융 기업을 위한 완벽 가이드

## 왜 지금 제로트러스트가 필요한가?

최근 사이버 보안 위협이 급증하면서...

[AI가 자동 생성한 전문적인 콘텐츠]
```

## 📁 프로젝트 구조

```
multi-channel-agent/
├── app.py                          # 메인 Streamlit 앱
├── src/
│   ├── agent_v2.py                 # 에이전트 오케스트레이션
│   ├── researcher.py               # LLM 기반 리서치
│   ├── content_generator_v2.py     # 콘텐츠 생성
│   ├── web_researcher.py           # 웹 검색
│   ├── reference_analyzer.py       # 레퍼런스 분석
│   ├── templates.py                # 템플릿 정의
│   └── publishers.py               # 포스팅 (개발 중)
├── requirements.txt                # 패키지 의존성
├── runtime.txt                     # Python 버전
├── .env.example                    # 환경 변수 예시
├── README.md                       # 이 파일
├── GROQ_SETUP_GUIDE.md            # Groq 설정 가이드
└── STREAMLIT_DEPLOY_GUIDE.md      # 배포 가이드
```

## 🐛 문제 해결

### Gemini 404 오류
```
Error calling model 'gemini-1.5-flash' (NOT_FOUND): 404
```

**해결책**: Groq로 전환하세요! [GROQ_SETUP_GUIDE.md](GROQ_SETUP_GUIDE.md) 참고

### OpenAI 할당량 초과
```
Error code: 429 - insufficient_quota
```

**해결책**: Groq (무료) 또는 Gemini로 전환

### 콘텐츠가 샘플 데이터
- 앱 상단에 "✅ Groq AI 연결됨" 메시지 확인
- API 키가 Secrets에 올바르게 설정되었는지 확인
- 앱 재시작

## 🔒 보안

- API 키는 절대 코드에 하드코딩하지 마세요
- `.env` 파일은 `.gitignore`에 포함
- Streamlit Cloud Secrets 사용 권장

## 📝 라이선스

MIT License

## 🤝 기여

이슈와 PR 환영합니다!

## 📞 지원

- GitHub Issues
- Groq Discord: https://discord.gg/groq

---

**Made with ❤️ for AI Hackathon**
