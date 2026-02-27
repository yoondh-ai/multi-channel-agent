"""각 플랫폼 퍼블리셔 모듈"""
import os
import tweepy
from typing import List

class TwitterPublisher:
    def __init__(self):
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_secret = os.getenv("TWITTER_API_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        
        self.client = None
        if all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            try:
                self.client = tweepy.Client(
                    consumer_key=self.api_key,
                    consumer_secret=self.api_secret,
                    access_token=self.access_token,
                    access_token_secret=self.access_token_secret
                )
            except Exception as e:
                print(f"Twitter 클라이언트 초기화 실패: {e}")
    
    def post_thread(self, tweets: List[str]) -> dict:
        """트위터 스레드 포스팅"""
        if not self.client:
            return {
                "success": False,
                "message": "Twitter API 설정이 필요합니다",
                "preview": tweets
            }
        
        try:
            previous_tweet_id = None
            posted_tweets = []
            
            for tweet in tweets:
                if len(tweet) > 280:
                    tweet = tweet[:277] + "..."
                
                response = self.client.create_tweet(
                    text=tweet,
                    in_reply_to_tweet_id=previous_tweet_id
                )
                previous_tweet_id = response.data['id']
                posted_tweets.append(response.data)
            
            return {
                "success": True,
                "message": f"{len(posted_tweets)}개의 트윗이 포스팅되었습니다",
                "tweet_ids": [t['id'] for t in posted_tweets]
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"포스팅 실패: {str(e)}",
                "preview": tweets
            }

class BlogPublisher:
    def __init__(self):
        self.medium_token = os.getenv("MEDIUM_ACCESS_TOKEN")
    
    def post_to_medium(self, title: str, content: str) -> dict:
        """Medium에 포스팅"""
        if not self.medium_token:
            return {
                "success": False,
                "message": "Medium API 토큰이 필요합니다",
                "preview": {
                    "title": title,
                    "content": content[:500] + "..."
                }
            }
        
        # Medium API 구현 (실제 API 호출)
        # 프로토타입에서는 미리보기만 제공
        return {
            "success": False,
            "message": "Medium API 연동 준비 중 (미리보기 모드)",
            "preview": {
                "title": title,
                "content": content
            }
        }
