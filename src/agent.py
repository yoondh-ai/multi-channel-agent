"""메인 에이전트 클래스"""
from .researcher import ContentResearcher
from .content_generator import ContentGenerator
from .publishers import TwitterPublisher, BlogPublisher

class MultiChannelAgent:
    def __init__(self):
        self.researcher = ContentResearcher()
        self.generator = ContentGenerator()
        self.twitter_publisher = TwitterPublisher()
        self.blog_publisher = BlogPublisher()
    
    def create_content_only(self, keywords: str, direction: str, channels: list, use_mock: bool = False) -> dict:
        """콘텐츠 생성만 수행 (포스팅 제외)"""
        
        results = {
            "research": None,
            "content": {}
        }
        
        if use_mock:
            # 데모 모드: 샘플 콘텐츠 생성
            print("🎭 데모 모드: 샘플 콘텐츠 생성 중...")
            results["research"] = {
                "raw_research": f"키워드 '{keywords}'에 대한 리서치 결과 (데모 모드)\n\n"
                               f"방향성: {direction}\n\n"
                               f"주요 포인트:\n"
                               f"1. 최신 보안 트렌드 반영\n"
                               f"2. 실무 적용 가능한 솔루션\n"
                               f"3. B2B 고객 맞춤 메시지",
                "keywords": keywords,
                "direction": direction
            }
            
            if "blog" in channels:
                results["content"]["blog"] = {
                    "title": f"{keywords}: 2024년 필수 보안 가이드",
                    "content": f"""# {keywords}의 모든 것

## 왜 지금 {keywords}가 중요한가?

{direction}

최근 사이버 보안 위협이 급증하면서 {keywords}에 대한 관심이 높아지고 있습니다. 특히 중소기업과 스타트업에서는 제한된 리소스로 효과적인 보안 체계를 구축해야 하는 과제에 직면해 있습니다.

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

{keywords}는 더 이상 선택이 아닌 필수입니다. 지금 바로 시작하세요!

---
*이 콘텐츠는 AI 에이전트가 자동 생성한 샘플입니다.*""",
                    "platform": "blog"
                }
            
            if "twitter" in channels:
                results["content"]["twitter"] = {
                    "tweets": [
                        f"🔐 {keywords}가 왜 중요할까요?\n\n{direction}\n\n최신 보안 트렌드를 쉽게 풀어드립니다 👇\n\n#보안 #사이버보안 #{keywords.replace(' ', '')}",
                        f"1️⃣ 첫 번째 핵심: 기본부터 탄탄하게\n\n보안의 시작은 현재 상태 파악입니다. 우리 회사의 보안 수준은 어느 정도일까요? 취약점을 먼저 찾아야 합니다.\n\n#보안전략 #IT보안",
                        f"2️⃣ 두 번째 핵심: 직원 교육\n\n기술만큼 중요한 것이 사람입니다. 정기적인 보안 교육으로 전 직원이 보안 의식을 갖추도록 해야 합니다.\n\n#보안교육 #정보보안",
                        f"3️⃣ 세 번째 핵심: 지속적 모니터링\n\n보안은 한 번 설정하고 끝이 아닙니다. 실시간 모니터링과 업데이트로 최신 위협에 대응하세요!\n\n💡 지금 바로 시작하세요!\n\n#보안솔루션 #사이버위협"
                    ],
                    "platform": "twitter"
                }
        else:
            # 실제 AI 모드
            # 1. 리서치
            print("🔍 리서치 중...")
            research_data = self.researcher.research_topic(keywords, direction)
            results["research"] = research_data
            
            # 2. 콘텐츠 생성
            print("✍️ 콘텐츠 생성 중...")
            
            if "blog" in channels:
                blog_content = self.generator.generate_blog_post(research_data)
                results["content"]["blog"] = blog_content
            
            if "twitter" in channels:
                twitter_content = self.generator.generate_twitter_thread(research_data)
                results["content"]["twitter"] = twitter_content
        
        return results
    
    def post_content(self, content: dict, channels: list) -> dict:
        """생성된 콘텐츠를 포스팅"""
        
        results = {}
        
        print("📤 포스팅 중...")
        
        if "blog" in channels and "blog" in content:
            blog_result = self.blog_publisher.post_to_medium(
                content["blog"]["title"],
                content["blog"]["content"]
            )
            results["blog"] = blog_result
        
        if "twitter" in channels and "twitter" in content:
            twitter_result = self.twitter_publisher.post_thread(
                content["twitter"]["tweets"]
            )
            results["twitter"] = twitter_result
        
        return results
    
    def create_and_post(self, keywords: str, direction: str, channels: list) -> dict:
        """콘텐츠 생성 및 포스팅 전체 프로세스 (기존 호환성 유지)"""
        
        results = {
            "research": None,
            "content": {},
            "posts": {}
        }
        
        # 1. 콘텐츠 생성
        content_results = self.create_content_only(keywords, direction, channels)
        results["research"] = content_results["research"]
        results["content"] = content_results["content"]
        
        # 2. 포스팅
        post_results = self.post_content(content_results["content"], channels)
        results["posts"] = post_results
        
        return results
