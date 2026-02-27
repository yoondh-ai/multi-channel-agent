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
    
    def create_content_only(self, keywords: str, direction: str, channels: list) -> dict:
        """콘텐츠 생성만 수행 (포스팅 제외)"""
        
        results = {
            "research": None,
            "content": {}
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
