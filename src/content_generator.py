"""채널별 콘텐츠 생성 모듈"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os

class ContentGenerator:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.8,
                api_key=api_key
            )
        else:
            self.llm = None
    
    def generate_blog_post(self, research_data: dict) -> dict:
        """블로그 포스트 생성"""
        
        if not self.llm:
            # API 키가 없으면 기본 콘텐츠 반환
            return {
                "title": "샘플 블로그 포스트",
                "content": "API 키를 설정하면 실제 AI 콘텐츠가 생성됩니다.",
                "platform": "blog"
            }
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 B2B 보안 분야의 전문 콘텐츠 작가입니다.
            트렌디하고 읽기 쉬운 블로그 포스트를 작성하세요."""),
            ("user", """리서치 데이터:
{research}

키워드: {keywords}
방향성: {direction}

다음 형식으로 블로그 포스트를 작성하세요:
- 제목: 클릭을 유도하는 매력적인 제목
- 본문: 1000-1500자, 섹션별로 구분
- SEO 키워드 자연스럽게 포함
- 실용적이고 가치 있는 정보 제공""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "research": research_data["raw_research"],
            "keywords": research_data["keywords"],
            "direction": research_data["direction"]
        })
        
        content = response.content
        lines = content.split('\n')
        title = lines[0].replace('제목:', '').replace('#', '').strip()
        body = '\n'.join(lines[1:]).strip()
        
        return {
            "title": title,
            "content": body,
            "platform": "blog"
        }
    
    def generate_twitter_thread(self, research_data: dict) -> dict:
        """트위터 스레드 생성"""
        
        if not self.llm:
            # API 키가 없으면 기본 콘텐츠 반환
            return {
                "tweets": ["샘플 트윗입니다. API 키를 설정하면 실제 AI 콘텐츠가 생성됩니다."],
                "platform": "twitter"
            }
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 소셜미디어 마케팅 전문가입니다.
            임팩트 있고 공유하고 싶은 트위터 스레드를 작성하세요."""),
            ("user", """리서치 데이터:
{research}

키워드: {keywords}
방향성: {direction}

트위터 스레드를 작성하세요:
- 첫 트윗: 강력한 훅 (280자 이내)
- 2-4개의 후속 트윗 (각 280자 이내)
- 이모지 활용
- 해시태그 포함
- 각 트윗을 [TWEET 1], [TWEET 2] 형식으로 구분""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "research": research_data["raw_research"],
            "keywords": research_data["keywords"],
            "direction": research_data["direction"]
        })
        
        # 트윗 분리
        content = response.content
        tweets = []
        current_tweet = []
        
        for line in content.split('\n'):
            if '[TWEET' in line.upper():
                if current_tweet:
                    tweets.append('\n'.join(current_tweet).strip())
                current_tweet = []
            else:
                current_tweet.append(line)
        
        if current_tweet:
            tweets.append('\n'.join(current_tweet).strip())
        
        return {
            "tweets": tweets,
            "platform": "twitter"
        }
