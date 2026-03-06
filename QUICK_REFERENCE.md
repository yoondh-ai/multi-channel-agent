# 빠른 참조 가이드 🚀

## 🎯 핵심 개선 사항 (한눈에 보기)

### ✅ UI 레이아웃
```
좌측 (1) : 우측 (1.2)
├─ 좌측: 콘텐츠 기획 폼
└─ 우측: 채널별 결과 탭
```

### ✅ 콘텐츠 품질
```
최소 글자 수:
- 블로그: 1,500자 이상
- LinkedIn: 800자 이상
- Twitter: 각 트윗 200자 이상
- 이메일: 500자 이상
```

### ✅ 프레임워크
```
PAS:  Problem (150자+) → Agitate (150자+) → Solution (200자+)
AIDA: Attention (100자+) → Interest (150자+) → Desire (150자+) → Action (100자+)
BAB:  Before (150자+) → After (150자+) → Bridge (200자+)
FAB:  Features (150자+) → Advantages (150자+) → Benefits (200자+)
```

---

## 🚀 빠른 시작

### 1. 실행
```bash
cd multi-channel-agent
streamlit run app.py
```

### 2. 테스트 입력
```
제품명: MarkAny 제로트러스트 솔루션
특징: 완벽한 보안, 클라우드 네이티브, AI 기반 위협 탐지
키워드: 제로트러스트, 클라우드 보안
프레임워크: PAS
```

### 3. 확인 사항
- [ ] 블로그 1,500자 이상
- [ ] 프레임워크 구조 명확
- [ ] 구체적 사례/수치 포함
- [ ] 키워드 자연스럽게 사용

---

## 📁 주요 파일

| 파일 | 역할 |
|------|------|
| `app.py` | 메인 UI (라인 186: 레이아웃) |
| `src/gemini_generator.py` | 콘텐츠 생성 로직 |
| `.kiro/steering/brand_voice.md` | 브랜드 가이드라인 |
| `.kiro/steering/content_guidelines.md` | 작성 가이드라인 |
| `src/templates.py` | 프레임워크 정의 |

---

## 🔧 주요 메서드

### gemini_generator.py
```python
_select_best_model()           # 자동 모델 선택
_load_brand_guidelines()       # 가이드라인 로드
_create_system_instruction()   # 시스템 지시 생성
_create_user_prompt()          # 사용자 프롬프트 생성
_get_framework_instructions()  # 프레임워크 지침
```

---

## 🐛 문제 해결

### 콘텐츠가 짧음
→ "추가 정보"에 더 많은 컨텍스트 입력

### 키워드만 반복
→ 프레임워크 변경 또는 말투를 "감성적"으로

### API 404 오류
→ 자동 모델 선택 기능이 해결 (재시작 필요 없음)

### UI 무너짐
→ `app.py` 라인 186 확인: `st.columns([1, 1.2])`

---

## 📊 품질 체크

### 필수 (Must Have)
- [x] 최소 글자 수 충족
- [x] 프레임워크 적용
- [x] 브랜드 톤 준수

### 우수 (Should Have)
- [x] 구체적 사례 포함
- [x] 수치 데이터 포함
- [x] 스토리텔링 요소

### 탁월 (Nice to Have)
- [x] 독창적 인사이트
- [x] 감정적 연결
- [x] 차별화된 관점

---

## 📚 문서

- `작업_완료_보고서.md`: 상세 작업 내용
- `IMPLEMENTATION_STATUS.md`: 구현 상태
- `TEST_GUIDE.md`: 테스트 가이드
- `GEMINI_SETUP_GUIDE.md`: API 설정

---

## ✅ 완료 확인

- [x] UI 레이아웃 1:1.2
- [x] 최소 글자 수 강제
- [x] 프레임워크 완벽 적용
- [x] 브랜드 가이드라인 주입
- [x] 마크다운 미리보기
- [x] 충분한 텍스트 높이 (500px)
- [x] Thinking Process 표시
- [x] 자동 모델 선택

**모든 작업 완료! 🎉**
