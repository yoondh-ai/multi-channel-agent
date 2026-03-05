"""개선된 마케팅 콘텐츠 생성 에이전트"""
from .researcher import ContentResearcher
from .content_generator_v2 import AdvancedContentGenerator
from .publishers import TwitterPublisher, BlogPublisher
from .reference_analyzer import ReferenceAnalyzer

class MarketingContentAgent:
    def __init__(self):
        self.researcher = ContentResearcher()
        self.generator = AdvancedContentGenerator()
        self.twitter_publisher = TwitterPublisher()
        self.blog_publisher = BlogPublisher()
        self.reference_analyzer = ReferenceAnalyzer()
    
    def generate_content(self, template: str, config: dict, use_mock: bool = False) -> list:
        """템플릿과 설정에 따라 여러 버전의 콘텐츠 생성"""
        
        variants = config.get('variants', 3)
        contents = []
        
        # 레퍼런스 분석
        reference_data = None
        if config.get('use_reference'):
            reference_data = self.reference_analyzer.get_reference_data(config)
            if reference_data:
                config['reference_data'] = reference_data
        
        if use_mock:
            # 데모 모드: 샘플 콘텐츠 생성
            for i in range(variants):
                content = self._generate_mock_content(template, config, i)
                contents.append(content)
        else:
            # 실제 AI 모드
            research_data = self.researcher.research_topic(
                config['keywords'],
                config['description']
            )
            
            for i in range(variants):
                content = self.generator.generate_by_template(
                    template=template,
                    research_data=research_data,
                    config=config,
                    variant=i
                )
                contents.append(content)
        
        return contents
    
    def _generate_mock_content(self, template: str, config: dict, variant: int) -> dict:
        """데모용 샘플 콘텐츠 생성"""
        
        keywords = config['keywords']
        tone = config['tone']
        audience = config['audience']
        brand = config.get('brand_name', 'MarkAny')
        
        # 템플릿별 샘플 콘텐츠
        if template == "blog_post":
            return {
                "title": f"{keywords}: {['완벽 가이드', '2024 트렌드', '실전 전략'][variant]}",
                "content": f"""# {keywords}의 모든 것

## 왜 지금 {keywords}가 중요한가?

{audience}를 위한 {tone} 가이드입니다.

최근 사이버 보안 위협이 급증하면서 {keywords}에 대한 관심이 높아지고 있습니다. {brand}는 이러한 변화에 발맞춰 혁신적인 솔루션을 제공합니다.

## 핵심 전략 3가지

### 1. 기본부터 탄탄하게
보안의 기본은 예방입니다. {keywords}를 도입하기 전에 현재 보안 상태를 점검하고, 취약점을 파악하는 것이 중요합니다.

### 2. 직원 교육이 핵심
아무리 좋은 보안 솔루션을 도입해도 직원들이 제대로 활용하지 못하면 무용지물입니다. 정기적인 보안 교육과 훈련이 필수입니다.

### 3. 지속적인 모니터링
보안은 한 번 설정하고 끝나는 것이 아닙니다. 실시간 모니터링과 정기적인 업데이트를 통해 최신 위협에 대응해야 합니다.

## 실무 적용 팁

- 단계별 로드맵 수립
- 예산에 맞는 솔루션 선택
- 전문가 자문 활용
- 정기적인 보안 점검

## 마치며

{keywords}는 더 이상 선택이 아닌 필수입니다. {brand}와 함께 안전한 디지털 환경을 만들어가세요.

{config.get('include_cta') and '**지금 바로 무료 상담 신청하기 →**' or ''}

---
*버전 {variant + 1} - AI 생성 콘텐츠*""",
                "seo_score": 85 + variant * 3,
                "readability": "높음"
            }
        
        elif template == "twitter_thread":
            return {
                "posts": [
                    f"🔐 {keywords}가 왜 중요할까요?\n\n{audience}라면 꼭 알아야 할 내용입니다 👇\n\n#{keywords.replace(' ', '')} #보안 #{brand}",
                    f"1️⃣ 첫 번째 핵심\n\n{tone} 관점에서 보면, 기본부터 탄탄하게 구축하는 것이 중요합니다.\n\n현재 보안 상태를 점검하고 취약점을 파악하세요.",
                    f"2️⃣ 두 번째 핵심\n\n직원 교육이 성공의 열쇠입니다.\n\n기술만큼 중요한 것이 사람입니다. 정기적인 보안 교육으로 전 직원이 보안 의식을 갖추도록 하세요.",
                    f"3️⃣ 세 번째 핵심\n\n지속적인 모니터링과 업데이트!\n\n보안은 한 번 설정하고 끝이 아닙니다. 실시간으로 위협을 감지하고 대응하세요.\n\n💡 {brand}가 도와드립니다!"
                ],
                "platform": "twitter"
            }
        
        elif template == "linkedin_post":
            return {
                "title": f"{keywords}: {audience}가 알아야 할 핵심",
                "content": f"""최근 {keywords} 관련 프로젝트를 진행하면서 얻은 인사이트를 공유합니다.

🔍 핵심 발견사항:

1. {tone} 접근이 성공의 열쇠
2. {audience}의 니즈를 정확히 파악
3. 실무 적용 가능한 솔루션 제공

{brand}는 이러한 원칙을 바탕으로 고객에게 최고의 가치를 제공합니다.

여러분의 경험은 어떠신가요? 댓글로 의견을 나눠주세요!

#{keywords.replace(' ', '')} #보안 #B2B #기술혁신""",
                "platform": "linkedin"
            }
        
        elif template == "marketing_email":
            return {
                "subject": f"[{brand}] {keywords} 완벽 가이드 - {audience} 필독",
                "preview": f"{keywords}로 비즈니스를 보호하세요",
                "content": f"""안녕하세요, {brand}입니다.

{audience}를 위한 특별한 소식을 전해드립니다.

## {keywords}의 중요성

최근 사이버 위협이 급증하면서 {keywords}에 대한 관심이 높아지고 있습니다.

## 우리의 솔루션

{brand}는 {tone} 접근 방식으로 다음을 제공합니다:

✓ 검증된 보안 솔루션
✓ 24/7 전문가 지원
✓ 맞춤형 컨설팅

## 특별 혜택

지금 신청하시면:
- 무료 보안 진단
- 30일 무료 체험
- 전문가 1:1 상담

[지금 바로 시작하기 →]

감사합니다.
{brand} 팀 드림

---
수신거부: [링크]""",
                "platform": "email"
            }
        
        elif template == "google_ads":
            return {
                "ads": [
                    {
                        "headline1": f"{keywords} 솔루션",
                        "headline2": f"{brand} 공식",
                        "headline3": "지금 무료 체험",
                        "description1": f"{audience}를 위한 최고의 보안 솔루션. 검증된 기술력.",
                        "description2": "30일 무료 체험. 전문가 상담 무료. 지금 시작하세요."
                    },
                    {
                        "headline1": f"{keywords} 전문가",
                        "headline2": "업계 1위 {brand}",
                        "headline3": "무료 상담 신청",
                        "description1": f"{tone} 솔루션으로 비즈니스를 보호하세요.",
                        "description2": "즉시 적용 가능. ROI 보장. 지금 문의하세요."
                    }
                ],
                "platform": "google_ads"
            }
        
        else:
            # 기본 템플릿
            return {
                "title": f"{keywords} - {brand}",
                "content": f"{audience}를 위한 {tone} 콘텐츠입니다.\n\n{keywords}에 대한 상세 정보를 제공합니다.",
                "platform": template
            }
    
    def post_content(self, content: dict, channels: list) -> dict:
        """생성된 콘텐츠를 포스팅"""
        
        results = {}
        
        if "blog" in channels and "content" in content:
            blog_result = self.blog_publisher.post_to_medium(
                content.get("title", "제목 없음"),
                content["content"]
            )
            results["blog"] = blog_result
        
        if "twitter" in channels and "posts" in content:
            twitter_result = self.twitter_publisher.post_thread(
                content["posts"]
            )
            results["twitter"] = twitter_result
        
        return results
