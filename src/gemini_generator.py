"""Google Gemini 2.0 Flash 기반 콘텐츠 생성기"""
import streamlit as st
import google.generativeai as genai
from pathlib import Path
from typing import Dict, List
import json
from src.templates import MARKETING_FRAMEWORKS

class GeminiContentGenerator:
    """Gemini 1.5 Flash를 사용한 고급 콘텐츠 생성기"""
    
    def __init__(self):
        """Gemini 초기화 및 가이드라인 로드"""
        self.model = None
        self.model_name = None
        
        # Streamlit Secrets에서 API 키 가져오기
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            
            # 사용 가능한 최적 모델 자동 선택
            self.model_name = self._select_best_model()
            
            if not self.model_name:
                print("⚠️ 사용 가능한 Gemini 모델을 찾을 수 없습니다")
                self.model = None
                return
            
            # 브랜드 가이드라인 로드
            self.brand_guidelines = self._load_brand_guidelines()
            
            # Gemini 모델 초기화 (system_instruction 포함)
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=self._create_system_instruction()
            )
            
            print(f"✅ Gemini {self.model_name} 연결됨 (무료)")
            
        except KeyError:
            print("⚠️ GEMINI_API_KEY가 st.secrets에 없습니다")
            self.model = None
        except Exception as e:
            print(f"⚠️ Gemini 초기화 실패: {e}")
            self.model = None
    
    def _select_best_model(self) -> str:
        """사용 가능한 최적의 Gemini 모델 자동 선택"""
        
        # 우선순위 순서로 시도할 모델 목록
        preferred_models = [
            'gemini-2.0-flash-exp',      # 최신 실험 버전
            'gemini-2.0-flash',           # Gemini 2.0 안정 버전
            'gemini-1.5-flash-latest',    # 1.5 최신 버전
            'gemini-1.5-flash',           # 1.5 기본 버전
            'gemini-1.5-flash-002',       # 1.5 특정 버전
            'gemini-pro',                 # 폴백 옵션
        ]
        
        try:
            # 사용 가능한 모델 목록 가져오기
            available_models = genai.list_models()
            available_model_names = [
                model.name.replace('models/', '') 
                for model in available_models 
                if 'generateContent' in model.supported_generation_methods
            ]
            
            print(f"📋 사용 가능한 모델: {', '.join(available_model_names[:5])}...")
            
            # 우선순위에 따라 사용 가능한 모델 선택
            for preferred in preferred_models:
                if preferred in available_model_names:
                    print(f"✅ 선택된 모델: {preferred}")
                    return preferred
            
            # 우선순위 목록에 없으면 첫 번째 사용 가능한 모델 선택
            if available_model_names:
                selected = available_model_names[0]
                print(f"⚠️ 기본 모델 사용: {selected}")
                return selected
            
            return None
            
        except Exception as e:
            print(f"⚠️ 모델 목록 조회 실패: {e}")
            # 실패 시 기본 모델 사용
            print("⚠️ 기본 모델 'gemini-1.5-flash' 사용 시도")
            return 'gemini-1.5-flash'
    
    def _load_brand_guidelines(self) -> str:
        """브랜드 가이드라인 문서 로드"""
        guidelines = []
        
        # .kiro/steering/ 디렉토리의 모든 마크다운 파일 로드
        steering_dir = Path(".kiro/steering")
        
        if steering_dir.exists():
            for md_file in sorted(steering_dir.glob("*.md")):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        guidelines.append(f"## {md_file.stem}\n\n{content}")
                        print(f"📋 가이드라인 로드: {md_file.name}")
                except Exception as e:
                    print(f"⚠️ {md_file} 로드 실패: {e}")
        
        if guidelines:
            return "\n\n---\n\n".join(guidelines)
        else:
            # 기본 가이드라인
            return """
# MarkAny 브랜드 가이드라인

## 브랜드 보이스
- 전문적이면서도 접근 가능한 톤
- 신뢰할 수 있고 혁신적인 이미지
- 고객 가치 중심의 커뮤니케이션

## 작성 원칙
- 데이터 기반 작성 (주어진 데이터에만 기반)
- 완전한 재작성 (단순 키워드 교체 금지)
- 고객 혜택 우선
"""
    
    def _create_system_instruction(self) -> str:
        """System Instruction 생성 (브랜드 가이드라인 포함)"""
        
        return f"""당신은 MarkAny의 전문 마케팅 콘텐츠 작성자입니다.

# 브랜드 가이드라인 (반드시 준수)

{self.brand_guidelines}

# 핵심 작성 원칙

## 1. 풍부한 콘텐츠 작성
- **최소 500자 이상** 작성 (블로그는 1,500자 이상)
- 단순 키워드 나열 금지
- 구체적인 설명과 예시 포함
- 스토리텔링 기법 활용

## 2. 마케팅 프레임워크 완벽 적용

### PAS (Problem-Agitate-Solution)
1. **Problem (문제 제기)**: 고객이 직면한 구체적 문제 상황 묘사 (150자 이상)
2. **Agitate (고통 증폭)**: 문제를 방치했을 때의 위험성과 손실 강조 (150자 이상)
3. **Solution (해결책)**: 제품/서비스가 어떻게 문제를 해결하는지 상세 설명 (200자 이상)

### AIDA (Attention-Interest-Desire-Action)
1. **Attention (주목)**: 강력한 훅으로 시선 끌기 (100자 이상)
2. **Interest (관심)**: 흥미로운 사실이나 통계로 관심 유발 (150자 이상)
3. **Desire (욕구)**: 제품 사용 후 얻을 수 있는 구체적 혜택 (150자 이상)
4. **Action (행동)**: 명확한 행동 유도 (100자 이상)

### BAB (Before-After-Bridge)
1. **Before (현재)**: 현재 상황의 문제점 (150자 이상)
2. **After (미래)**: 개선된 이상적 상황 (150자 이상)
3. **Bridge (연결)**: 어떻게 그 미래에 도달할 수 있는지 (200자 이상)

### FAB (Features-Advantages-Benefits)
1. **Features (기능)**: 제품의 구체적 기능 설명 (150자 이상)
2. **Advantages (장점)**: 경쟁사 대비 우위 (150자 이상)
3. **Benefits (혜택)**: 고객이 얻는 실질적 가치 (200자 이상)

## 3. 콘텐츠 구조

### 블로그 포스트 (1,500-2,500자)
```
# 매력적인 제목 (호기심 유발)

## 도입부 (200-300자)
- 현재 상황/문제 제기
- 독자 공감 유도
- 글의 방향 제시

## 본문 (1,000-1,500자)
### 소제목 1: 문제 상황
- 구체적 사례
- 통계 데이터
- 고객 pain point

### 소제목 2: 해결 방법
- 제품/서비스 소개
- 핵심 기능 설명
- 차별화 포인트

### 소제목 3: 실제 효과
- 성공 사례
- 구체적 수치
- 고객 후기

## 결론 (200-300자)
- 핵심 메시지 요약
- 행동 유도 (CTA)
- 다음 단계 안내
```

### LinkedIn 포스트 (800-1,200자)
```
[강력한 훅] (50자)
독자의 주목을 끄는 질문이나 통계

[인사이트] (200-300자)
최근 트렌드나 발견한 사실

[개인적 경험] (200-300자)
관련된 경험이나 관찰

[비즈니스 임팩트] (200-300자)
왜 이것이 중요한지, 어떤 가치가 있는지

[질문] (50자)
독자 참여 유도

#해시태그 #3개에서5개
```

### Twitter 스레드 (3-7개 트윗)
```
[트윗 1] 🔥 강력한 훅 (250자)
충격적 통계나 질문으로 시작

[트윗 2] 📊 문제 상황 (250자)
현재 직면한 문제 설명

[트윗 3] 💡 해결책 (250자)
핵심 아이디어 제시

[트윗 4] ✅ 구체적 방법 (250자)
실행 가능한 팁

[트윗 5] 🎯 CTA (250자)
행동 유도 및 링크
```

### 마케팅 이메일 (500-800자)
```
제목: [호기심 유발] (50자 이내)

프리헤더: [제목 보완] (100자 이내)

안녕하세요, [개인화 인사] (50자)

[가치 제안] (150-200자)
핵심 혜택 명확히 제시

[증거] (200-300자)
- 구체적 수치
- 고객 사례
- 사회적 증거

[CTA] (100자)
명확한 행동 유도

감사합니다.
[서명]
```

## 4. 작성 시 반드시 포함할 요소

### 구체성
- ❌ "보안이 강화됩니다"
- ✅ "보안 사고가 평균 73% 감소하고, 위협 탐지 시간이 5분에서 30초로 단축됩니다"

### 스토리텔링
- ❌ "좋은 제품입니다"
- ✅ "A사는 랜섬웨어 공격으로 3일간 업무가 마비되었습니다. 복구 비용만 2억원이 들었죠. 하지만 B사는..."

### 감정 연결
- ❌ "효율적입니다"
- ✅ "이제 밤에 보안 걱정 없이 편히 주무실 수 있습니다"

### 데이터 활용
- 통계: "최근 조사에 따르면 기업의 68%가..."
- 수치: "도입 후 3개월 만에 ROI 250% 달성"
- 비교: "기존 대비 5배 빠른 처리 속도"

## 5. 금지 사항

### 절대 하지 말 것
- ❌ 키워드만 반복 나열
- ❌ 짧고 성의 없는 문장
- ❌ 추상적이고 모호한 표현
- ❌ 근거 없는 과장
- ❌ 500자 미만의 짧은 콘텐츠

### 반드시 할 것
- ✅ 구체적인 사례와 수치
- ✅ 고객 관점의 혜택 설명
- ✅ 스토리텔링 기법 활용
- ✅ 감정적 연결 시도
- ✅ 명확한 구조와 흐름

## 6. 출력 형식

반드시 다음 JSON 형식으로 응답:

```json
{{
  "thinking": {{
    "target_audience": "타겟 독자 상세 분석 (100자 이상)",
    "core_value": "핵심 가치 제안 (100자 이상)",
    "key_message": "전달할 핵심 메시지 (100자 이상)",
    "differentiation": "차별화 포인트 (100자 이상)",
    "framework_application": "선택된 프레임워크 적용 방법 (100자 이상)"
  }},
  "content": {{
    "title": "매력적인 제목 (호기심 유발)",
    "body": "본문 내용 (최소 500자, 블로그는 1,500자 이상)",
    "cta": "명확한 행동 유도 문구"
  }},
  "metadata": {{
    "tone": "사용된 톤",
    "word_count": 실제_글자_수,
    "key_points": ["핵심 포인트 1", "핵심 포인트 2", "핵심 포인트 3"],
    "framework_used": "적용된 프레임워크"
  }}
}}
```

## 7. 품질 체크리스트

작성 후 반드시 확인:
- [ ] 최소 글자 수 충족 (블로그 1,500자, 기타 500자)
- [ ] 마케팅 프레임워크 완벽 적용
- [ ] 구체적 사례나 수치 포함
- [ ] 스토리텔링 요소 포함
- [ ] 고객 혜택 명확히 제시
- [ ] 감정적 연결 시도
- [ ] 명확한 CTA 포함
- [ ] 브랜드 톤 준수

중요: 반드시 유효한 JSON 형식으로만 응답하세요.
"""
    
    def generate_content(
        self,
        template: str,
        config: Dict
    ) -> Dict:
        """콘텐츠 생성"""
        
        if not self.model:
            return self._generate_fallback_content(template, config)
        
        try:
            # 채널 정보
            channel_info = self._get_channel_info(template)
            
            # User Prompt 생성 (소스 데이터 최상단 배치)
            user_prompt = self._create_user_prompt(config, channel_info)
            
            # Gemini 호출
            response = self.model.generate_content(user_prompt)
            
            # 응답 파싱
            result = self._parse_response(response.text, template)
            
            return result
            
        except Exception as e:
            print(f"⚠️ Gemini 생성 실패: {e}")
            return self._generate_fallback_content(template, config)
    
    def _create_user_prompt(self, config: Dict, channel_info: Dict) -> str:
        """User Prompt 생성 (소스 데이터를 최상단에 배치)"""
        
        # 프레임워크 상세 정보
        framework = config.get('framework', 'PAS')
        framework_info = MARKETING_FRAMEWORKS.get(framework, {})
        
        return f"""# 소스 데이터 (이 데이터를 바탕으로 풍부한 콘텐츠 작성)

## 제품/서비스 정보
**제품명**: {config.get('product_name', 'N/A')}

## 핵심 특징 (이것을 바탕으로 구체적 설명 작성)
{config.get('key_features', 'N/A')}

## 타겟 키워드 (자연스럽게 녹여서 사용)
{config.get('keywords', 'N/A')}

## 추가 정보 (이것을 활용하여 스토리텔링)
{config.get('additional_context', '없음')}

---

# 작성 요구사항

## 채널 정보
- **채널**: {channel_info['name']}
- **권장 길이**: {channel_info['length']}
- **톤**: {channel_info['tone']}

## 타겟 독자
**대상**: {config.get('audience', 'IT 담당자')}

이 독자들은:
- 전문적인 정보를 원함
- 구체적인 수치와 사례를 중요시함
- 비즈니스 가치에 관심이 많음

## 말투 (Tone)
**톤**: {config.get('tone', '전문적')}

## 마케팅 프레임워크
**프레임워크**: {framework_info.get('name', framework)}
**설명**: {framework_info.get('description', '')}
**구조**: {' → '.join(framework_info.get('structure', []))}

이 프레임워크를 **완벽하게** 적용하여 작성하세요.

## 콘텐츠 길이
**목표**: {config.get('length', '보통')}
**최소 글자 수**: 
- 블로그 포스트: 1,500자 이상
- LinkedIn: 800자 이상
- Twitter: 각 트윗 200자 이상
- 이메일: 500자 이상

## 추가 옵션
- **SEO 최적화**: {config.get('include_seo', True)}
- **CTA 포함**: {config.get('include_cta', True)}

---

# 작성 지시 (반드시 준수)

## 1단계: Thinking Process (내부 사고)
다음을 깊이 분석하세요:
- 타겟 독자의 pain point는 무엇인가?
- 이 제품/서비스가 어떤 가치를 제공하는가?
- 왜 지금 이것이 필요한가?
- 어떻게 차별화할 것인가?

## 2단계: 프레임워크 적용
{framework} 프레임워크의 각 단계를 **구체적으로** 작성:

{self._get_framework_instructions(framework)}

## 3단계: 풍부한 콘텐츠 작성
다음을 반드시 포함:

### 구체적 사례
- "예를 들어, A사는..." 형식의 실제 사례
- 구체적인 상황 묘사
- 독자가 공감할 수 있는 스토리

### 수치와 데이터
- "평균 73% 감소" 같은 구체적 수치
- "3개월 만에 ROI 250%" 같은 성과
- "업계 68%가 직면한 문제" 같은 통계

### 감정적 연결
- 독자의 고민과 걱정 공감
- 해결 후의 긍정적 미래 제시
- "이제 안심하고..." 같은 감정 표현

### 명확한 구조
- 도입 → 본론 → 결론
- 각 섹션마다 소제목
- 논리적 흐름

## 4단계: 품질 검증
작성 후 확인:
- [ ] 최소 글자 수 충족?
- [ ] 프레임워크 완벽 적용?
- [ ] 구체적 사례 포함?
- [ ] 수치 데이터 포함?
- [ ] 감정적 연결 시도?
- [ ] 명확한 CTA?

---

# 중요 알림

⚠️ **키워드만 반복하지 마세요!**
❌ 나쁜 예: "제로트러스트는 좋습니다. 제로트러스트를 사용하세요."
✅ 좋은 예: "최근 원격 근무가 확대되면서 기업 보안의 패러다임이 바뀌고 있습니다. 전통적인 경계 기반 보안으로는 더 이상 충분하지 않죠. 바로 이 지점에서 제로트러스트가 주목받고 있습니다. '아무도 믿지 않고, 모든 것을 검증한다'는 원칙..."

⚠️ **최소 500자 이상 작성하세요!**
블로그는 1,500자 이상 필수입니다.

⚠️ **스토리텔링을 활용하세요!**
단순 설명이 아닌, 독자가 공감할 수 있는 이야기를 만드세요.

반드시 JSON 형식으로 응답하세요.
"""
    
    def _get_framework_instructions(self, framework: str) -> str:
        """프레임워크별 상세 작성 지침"""
        
        instructions = {
            "PAS": """
**Problem (문제 제기)** - 150자 이상
- 독자가 직면한 구체적 문제 상황
- "혹시 이런 경험 있으신가요?" 형식
- 공감할 수 있는 사례

**Agitate (고통 증폭)** - 150자 이상
- 문제를 방치했을 때의 위험
- 구체적인 손실 (시간, 비용, 기회)
- "만약 ~한다면..." 형식

**Solution (해결책)** - 200자 이상
- 제품/서비스가 어떻게 해결하는지
- 구체적인 기능과 효과
- 실제 성과 수치
""",
            "AIDA": """
**Attention (주목)** - 100자 이상
- 충격적 통계나 질문
- "알고 계셨나요?" 형식
- 호기심 유발

**Interest (관심)** - 150자 이상
- 흥미로운 사실이나 트렌드
- 독자와의 관련성 강조
- "이것이 중요한 이유는..." 형식

**Desire (욕구)** - 150자 이상
- 제품 사용 후의 긍정적 변화
- 구체적 혜택 나열
- "상상해보세요..." 형식

**Action (행동)** - 100자 이상
- 명확한 다음 단계
- 긴급성 조성
- "지금 바로..." 형식
""",
            "BAB": """
**Before (현재)** - 150자 이상
- 현재 상황의 문제점
- 독자의 고민 공감
- 구체적 pain point

**After (미래)** - 150자 이상
- 개선된 이상적 상황
- 긍정적 변화 묘사
- 구체적 혜택

**Bridge (연결)** - 200자 이상
- 어떻게 그 미래에 도달하는지
- 제품/서비스의 역할
- 실행 가능한 단계
""",
            "FAB": """
**Features (기능)** - 150자 이상
- 제품의 구체적 기능
- 기술적 특징
- "~할 수 있습니다" 형식

**Advantages (장점)** - 150자 이상
- 경쟁사 대비 우위
- 독특한 차별점
- "다른 제품과 달리..." 형식

**Benefits (혜택)** - 200자 이상
- 고객이 얻는 실질적 가치
- 비즈니스 임팩트
- ROI, 시간 절감 등 구체적 수치
"""
        }
        
        return instructions.get(framework, "프레임워크 구조에 맞춰 작성하세요.")
    
    def _parse_response(self, response: str, template: str) -> Dict:
        """Gemini 응답을 파싱하여 구조화된 데이터로 변환"""
        
        try:
            # JSON 추출 (```json ... ``` 형식 처리)
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            else:
                json_str = response.strip()
            
            # JSON 파싱
            data = json.loads(json_str)
            
            # 템플릿에 맞게 변환
            if template == "blog_post":
                return {
                    "title": data['content'].get('title', '제목 없음'),
                    "content": data['content'].get('body', ''),
                    "platform": "blog",
                    "thinking": data.get('thinking', {}),
                    "metadata": data.get('metadata', {}),
                    "seo_score": 85,
                    "readability": "높음"
                }
            elif template == "twitter_thread":
                body = data['content'].get('body', '')
                tweets = self._split_into_tweets(body)
                return {
                    "posts": tweets,
                    "platform": "twitter",
                    "thinking": data.get('thinking', {}),
                    "metadata": data.get('metadata', {}),
                    "seo_score": 80,
                    "readability": "높음"
                }
            elif template == "linkedin_post":
                return {
                    "content": data['content'].get('body', ''),
                    "platform": "linkedin",
                    "thinking": data.get('thinking', {}),
                    "metadata": data.get('metadata', {}),
                    "seo_score": 85,
                    "readability": "높음"
                }
            elif template == "marketing_email":
                return {
                    "subject": data['content'].get('title', '제목 없음'),
                    "content": data['content'].get('body', ''),
                    "platform": "email",
                    "thinking": data.get('thinking', {}),
                    "metadata": data.get('metadata', {}),
                    "seo_score": 80,
                    "readability": "높음"
                }
            else:
                return {
                    "content": data['content'].get('body', ''),
                    "platform": template,
                    "thinking": data.get('thinking', {}),
                    "metadata": data.get('metadata', {})
                }
                
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON 파싱 실패: {e}")
            # 파싱 실패 시 원문 반환
            return {
                "content": response,
                "platform": template,
                "error": "JSON 파싱 실패",
                "seo_score": 75,
                "readability": "보통"
            }
    
    def _split_into_tweets(self, text: str) -> List[str]:
        """긴 텍스트를 트윗으로 분할"""
        tweets = []
        paragraphs = text.split('\n\n')
        
        current_tweet = ""
        for para in paragraphs:
            if len(current_tweet) + len(para) + 2 <= 280:
                current_tweet += para + "\n\n"
            else:
                if current_tweet:
                    tweets.append(current_tweet.strip())
                current_tweet = para + "\n\n"
        
        if current_tweet:
            tweets.append(current_tweet.strip())
        
        return tweets if tweets else [text[:280]]
    
    def _get_channel_info(self, template: str) -> Dict:
        """채널 정보 반환"""
        channels = {
            "blog_post": {
                "name": "블로그 포스트",
                "length": "1,500-2,500자",
                "tone": "전문적, 교육적"
            },
            "twitter_thread": {
                "name": "Twitter 스레드",
                "length": "3-7개 트윗",
                "tone": "간결, 임팩트"
            },
            "linkedin_post": {
                "name": "LinkedIn 포스트",
                "length": "800-1,200자",
                "tone": "전문적, 인사이트 중심"
            },
            "marketing_email": {
                "name": "마케팅 이메일",
                "length": "500-800자",
                "tone": "친근하면서 전문적"
            }
        }
        return channels.get(template, {"name": template, "length": "보통", "tone": "전문적"})
    
    def _generate_fallback_content(self, template: str, config: Dict) -> Dict:
        """Gemini 사용 불가 시 폴백 콘텐츠"""
        product_name = config.get('product_name', 'MarkAny 솔루션')
        
        return {
            "title": f"{product_name} 소개",
            "content": f"""# {product_name}

{config.get('key_features', '혁신적인 보안 솔루션')}

{config.get('additional_context', '')}

지금 바로 문의하세요!""",
            "platform": template,
            "note": "Gemini 사용 불가 - 폴백 콘텐츠",
            "seo_score": 70,
            "readability": "보통"
        }
