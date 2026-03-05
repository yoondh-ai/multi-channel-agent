# Groq 지원 모델 (2024년 최신)

## 🎯 현재 사용 중인 모델

**llama-3.3-70b-versatile** ✅

- 가장 강력한 무료 모델
- 70B 파라미터
- 한국어 우수
- 마케팅 콘텐츠 생성에 최적

## 📋 Groq 사용 가능한 모델 목록

### Llama 시리즈 (Meta)

| 모델 ID | 파라미터 | 속도 | 추천 용도 |
|---------|----------|------|-----------|
| **llama-3.3-70b-versatile** | 70B | ⚡⚡⚡ | 마케팅, 긴 콘텐츠 ⭐ |
| llama-3.1-8b-instant | 8B | ⚡⚡⚡⚡ | 빠른 응답, 짧은 콘텐츠 |
| llama3-70b-8192 | 70B | ⚡⚡⚡ | 복잡한 작업 |
| llama3-8b-8192 | 8B | ⚡⚡⚡⚡ | 일반 작업 |

### Mixtral 시리즈 (Mistral AI)

| 모델 ID | 파라미터 | 속도 | 추천 용도 |
|---------|----------|------|-----------|
| mixtral-8x7b-32768 | 8x7B | ⚡⚡⚡ | 다국어, 코드 |
| mixtral-8x22b-32768 | 8x22B | ⚡⚡ | 고급 추론 |

### Gemma 시리즈 (Google)

| 모델 ID | 파라미터 | 속도 | 추천 용도 |
|---------|----------|------|-----------|
| gemma2-9b-it | 9B | ⚡⚡⚡ | 일반 작업 |
| gemma-7b-it | 7B | ⚡⚡⚡⚡ | 빠른 응답 |

## 🔄 모델 변경 방법

### 코드에서 변경

`src/researcher.py`와 `src/content_generator_v2.py`에서:

```python
self.llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # 여기를 변경
    temperature=0.7,
    groq_api_key=groq_key
)
```

### 추천 설정

#### 최고 품질 (현재 설정)
```python
model="llama-3.3-70b-versatile"
temperature=0.7  # 창의성과 일관성 균형
```

#### 최고 속도
```python
model="llama-3.1-8b-instant"
temperature=0.7
```

#### 다국어 최적화
```python
model="mixtral-8x7b-32768"
temperature=0.7
```

## 📊 성능 비교 (마케팅 콘텐츠 생성)

### 500자 블로그 포스트 생성

| 모델 | 속도 | 품질 | 한국어 | 추천 |
|------|------|------|--------|------|
| llama-3.3-70b-versatile | 2-3초 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ |
| llama-3.1-8b-instant | 1-2초 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 빠른 작업 |
| mixtral-8x7b-32768 | 2-4초 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 다국어 |

## 🚨 중단된 모델 (사용 불가)

- ❌ llama-3.1-70b-versatile (2024년 중단)
- ❌ llama-3.1-405b-reasoning (2024년 중단)

## 💡 모델 선택 가이드

### 마케팅 콘텐츠 생성 (현재 프로젝트)
→ **llama-3.3-70b-versatile** ✅
- 긴 형식 콘텐츠
- 창의적 글쓰기
- 한국어 우수

### SNS 짧은 포스트
→ **llama-3.1-8b-instant**
- 빠른 생성
- 여러 버전 동시 생성
- 충분한 품질

### 다국어 콘텐츠
→ **mixtral-8x7b-32768**
- 영어, 한국어, 일본어 등
- 번역 작업
- 글로벌 마케팅

## 🔧 고급 설정

### Temperature 조정

```python
# 더 창의적 (다양한 표현)
temperature=0.9

# 균형 (추천)
temperature=0.7

# 더 일관적 (정확한 정보)
temperature=0.5
```

### Max Tokens 설정

```python
self.llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    max_tokens=2000,  # 최대 출력 길이
    groq_api_key=groq_key
)
```

## 📈 사용량 제한

Groq 무료 티어:
- 분당 요청: 30회
- 일일 요청: 14,400회
- 토큰 제한: 없음

**충분히 넉넉합니다!** 해커톤 데모에 완벽.

## 🔍 최신 정보 확인

공식 문서:
- https://console.groq.com/docs/models
- https://console.groq.com/docs/deprecations

## 💬 추천 설정 (요약)

현재 프로젝트에 최적:

```python
# researcher.py & content_generator_v2.py
ChatGroq(
    model="llama-3.3-70b-versatile",  # 최신, 최고 품질
    temperature=0.7,                   # 창의성과 일관성 균형
    groq_api_key=groq_key
)
```

이 설정으로:
- ✅ 고품질 한국어 콘텐츠
- ✅ 빠른 생성 속도 (2-3초)
- ✅ 완전 무료
- ✅ 안정적

---

*마지막 업데이트: 2024년 3월*
