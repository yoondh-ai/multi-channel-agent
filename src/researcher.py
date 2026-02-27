"""웹 리서치 및 트렌드 분석 모듈"""
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

class ContentResearcher:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def research_topic(self, keywords: str, direction: str) -> dict:
        """키워드와 방향성을 기반으로 콘텐츠 리서치"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 B2B 보안 마케팅 전문가입니다. 
            주어진 키워드와 방향성을 바탕으로 트렌디하고 매력적인 콘텐츠 아이디어를 제공하세요."""),
            ("user", """키워드: {keywords}
방향성: {direction}

다음 정보를 JSON 형식으로 제공하세요:
1. 핵심 메시지 (key_message)
2. 타겟 독자 (target_audience)
3. 주요 포인트 3가지 (main_points - 리스트)
4. 추천 해시태그 (hashtags - 리스트)
5. 콘텐츠 톤 (tone)""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "keywords": keywords,
            "direction": direction
        })
        
        # 간단한 파싱 (실제로는 JSON 파싱 필요)
        return {
            "raw_research": response.content,
            "keywords": keywords,
            "direction": direction
        }
