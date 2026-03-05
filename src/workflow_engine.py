"""3단계 워크플로우 엔진"""
import os
from langchain_core.prompts import ChatPromptTemplate

class WorkflowEngine:
    def __init__(self, llm):
        self.llm = llm
        self.brand_guide = self._load_brand_guide()
        self.channel_guide = self._load_channel_guide()
    
    def _load_brand_guide(self) -> str:
        """브랜드 가이드 로드"""
        try:
            with open('brand_identity.md', 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return "MarkAny: 디지털 보안 전문 기업, 혁신/신뢰/전문성 핵심 가치"
    
    def _load_channel_guide(self) -> str:
        """채널 가이드라인 로드"""
        try:
            with open('channel_guidelines.md', 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return "채널별 최적화 가이드라인"
    
    def step1_analyze_usp(self, product_info: dict) -> dict:
        """
        Step 1: USP 분석
        사용자 입력 정보를 바탕으로 브랜드 가이드에 맞춰 핵심 소구점 정리
        """
        if not self.llm:
            # 데모 모드
            return {
                "usp_summary": f"""
## 핵심 소구점 (USP) 분석

### 제품: {product_info['product_name']}

#### 1. 주요 차별점
• 검증된 보안 기술력
• 빠른 도입 및 ROI
• 24/7 전문가 지원

#### 2. 타겟 고객 혜택
• {product_info['audience']}: 안정적이고 신뢰할 수 있는 보안 솔루션
• 비즈니스 연속성 보장
• 규제 준수 지원

#### 3. 핵심 메시지
"{product_info['product_name']}로 디지털 자산을 완벽하게 보호하세요"

#### 4. 감성적 소구
• 안심: 검증된 기술로 걱정 없이
• 신뢰: 20년 이상의 전문성
• 혁신: 최신 기술 트렌드 반영
""",
                "key_messages": [
                    "검증된 보안 기술력",
                    "빠른 도입 및 ROI",
                    "24/7 전문가 지원"
                ],
                "target_benefits": f"{product_info['audience']}를 위한 맞춤형 솔루션",
                "emotional_appeal": "안심과 신뢰"
            }
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""당신은 MarkAny의 브랜드 전략가입니다.

브랜드 가이드:
{self.brand_guide}

위 브랜드 아이덴티티를 바탕으로 제품의 핵심 소구점(USP)을 분석하세요."""),
            ("user", """제품 정보:
- 제품명: {product_name}
- 핵심 특징: {features}
- 타겟 독자: {audience}
- 키워드: {keywords}
- 추가 정보: {context}

다음 형식으로 USP를 분석하세요:

## 핵심 소구점 (USP) 분석

### 1. 주요 차별점
(경쟁사 대비 3가지 핵심 차별점)

### 2. 타겟 고객 혜택
(타겟 독자가 얻을 구체적 혜택)

### 3. 핵심 메시지
(한 문장으로 요약)

### 4. 감성적 소구
(고객의 감정에 호소하는 요소)
""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "product_name": product_info['product_name'],
            "features": product_info['features'],
            "audience": product_info['audience'],
            "keywords": product_info['keywords'],
            "context": product_info.get('context', '')
        })
        
        return {
            "usp_summary": response.content,
            "raw_response": response.content
        }
    
    def step2_generate_drafts(self, usp_analysis: dict, config: dict) -> dict:
        """
        Step 2: 초안 생성
        선택된 프레임워크(PAS/AIDA)에 맞춰 4개 채널용 초안 동시 생성
        """
        if not self.llm:
            # 데모 모드
            return {
                "네이버 블로그": self._mock_blog_draft(config),
                "LinkedIn": self._mock_linkedin_draft(config),
                "Twitter": self._mock_twitter_draft(config),
                "이메일": self._mock_email_draft(config)
            }
        
        framework = config.get('framework', 'PAS')
        framework_structure = self._get_framework_structure(framework)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""당신은 멀티채널 마케팅 콘텐츠 전문가입니다.

마케팅 프레임워크: {framework}
구조: {framework_structure}

USP 분석 결과:
{usp_analysis['usp_summary']}

위 USP를 바탕으로 {framework} 프레임워크에 맞춰 콘텐츠를 작성하세요."""),
            ("user", """다음 4개 채널용 초안을 동시에 생성하세요:

설정:
- 타겟: {audience}
- 톤: {tone}
- 키워드: {keywords}

각 채널별로 {framework} 구조를 따르되, 채널 특성에 맞게 조정하세요.

형식:
## 네이버 블로그
[제목]
[본문 - 1500자 내외]

## LinkedIn
[본문 - 800자 내외]

## Twitter
[트윗 1]
[트윗 2]
[트윗 3]
[트윗 4]

## 이메일
[제목]
[본문 - 500자 내외]
""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "framework": framework,
            "audience": config['audience'],
            "tone": config['tone']