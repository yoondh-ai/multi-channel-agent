"""Google Gemini 1.5 Flash 기반 콘텐츠 생성기"""
import streamlit as st
import google.generativeai as genai
from pathlib import Path
from typing import Dict, List
import json

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

## 1. Thinking Process (사고 과정)
글을 쓰기 전 반드시 다음을 분석:

### 타겟 분석
- 이 글의 주요 독자는 누구인가?
- 그들의 주요 관심사와 니즈는?
- 그들의 전문성 수준은?

### 핵심 가치 정의
- 이 글에서 전달할 핵심 메시지는?
- 독자가 얻을 수 있는 구체적 가치는?
- 왜 지금 이 내용이 중요한가?

### 차별화 포인트
- 이 콘텐츠만의 독특한 가치는?
- 독자의 주목을 끌 요소는?

## 2. 데이터 기반 작성 (Data-Grounded)
- 사용자가 제공한 소스 데이터에만 기반하여 작성
- 외부 지식이나 가정을 추가하지 말 것
- 주어진 데이터에 없는 내용은 작성하지 말 것

## 3. 완전한 재작성 (Full Paraphrasing)
- 단순히 키워드만 바꾸지 말 것
- 문장 구조를 완전히 새로 구성
- 동일한 의미를 다른 방식으로 표현
- 원문의 흐름을 그대로 따르지 말 것

## 4. 브랜드 톤 준수
- MarkAny 브랜드 가이드라인 철저히 준수
- 전문적이면서도 접근 가능한 톤
- 고객 가치 중심의 메시지

## 5. 출력 형식
반드시 다음 JSON 형식으로 응답:

```json
{{
  "thinking": {{
    "target_audience": "타겟 독자 분석",
    "core_value": "핵심 가치",
    "key_message": "핵심 메시지",
    "differentiation": "차별화 포인트"
  }},
  "content": {{
    "title": "제목 (해당되는 경우)",
    "body": "본문 내용",
    "cta": "행동 유도 문구"
  }},
  "metadata": {{
    "tone": "사용된 톤",
    "word_count": 글자 수,
    "key_points": ["핵심 포인트 1", "핵심 포인트 2"]
  }}
}}
```

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
        
        return f"""# 소스 데이터 (이 데이터에만 기반하여 작성)

## 제품/서비스 정보
제품명: {config.get('product_name', 'N/A')}

## 핵심 특징
{config.get('key_features', 'N/A')}

## 타겟 키워드
{config.get('keywords', 'N/A')}

## 추가 정보
{config.get('additional_context', '없음')}

---

# 작성 요구사항

## 채널
{channel_info['name']} ({channel_info['length']})

## 타겟 독자
{config.get('audience', 'IT 담당자')}

## 톤앤매너
{config.get('tone', '전문적')} - {channel_info['tone']}

## 마케팅 프레임워크
{config.get('framework', 'PAS')}

## 콘텐츠 길이
{config.get('length', '보통')}

## 추가 옵션
- SEO 최적화: {config.get('include_seo', True)}
- CTA 포함: {config.get('include_cta', True)}

---

# 작성 지시

위의 소스 데이터를 바탕으로, 다음 단계를 거쳐 콘텐츠를 작성하세요:

1. **Thinking Process**: 타겟 분석, 핵심 가치 정의, 차별화 포인트 파악
2. **완전한 재작성**: 문장 구조를 완전히 새로 구성 (단순 키워드 교체 금지)
3. **데이터 기반**: 주어진 소스 데이터에만 기반 (외부 지식 추가 금지)
4. **브랜드 톤 준수**: MarkAny 브랜드 가이드라인 준수

반드시 JSON 형식으로 응답하세요.
"""
    
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
