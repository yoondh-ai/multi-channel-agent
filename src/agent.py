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
    
    def create_and_post(self, keywords: str, direction: str, channels: list) -> dict:
        """콘텐츠 생성 및 포스팅 전체 프로세스"""
        
        results = {
            "research": None,
            "content": {},
            "posts": {}
        }
        
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
        
        # 3. 포스팅
        print("📤 포스팅 중...")
        
        if "blog" in channels and "blog" in results["content"]:
            blog_result = self.blog_publisher.post_to_medium(
                results["content"]["blog"]["title"],
                results["content"]["blog"]["content"]
            )
            results["posts"]["blog"] = blog_result
        
        if "twitter" in channels and "twitter" in results["content"]:
            twitter_result = self.twitter_publisher.post_thread(
                results["content"]["twitter"]["tweets"]
            )
            results["posts"]["twitter"] = twitter_result
        
        return results
