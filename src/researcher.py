"""웹 리서치 및 트렌드 분석 모듈"""
import os

class ContentResearcher:
    def __init__(self):
        # OpenAI 또는 Gemini 선택
        self.api_provider = None
        self.llm = None
        
        openai_key = os.getenv("OPENAI_API_KEY")
        gemini_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        
        if gemini_key:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                self.llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    temperature=0.7,
                    google_api_key=gemini_key
                )
                self.api_provider = "gemini"
                print("✅ Gemini API 연결됨")
            except Exception as e:
                print(f"Gemini 초기화 실패: {e}")
        
        if not self.llm and openai_key:
            try:
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0.7,
                    api_key=openai_key
                )
                self.api_provider = "openai"
                print("✅ OpenAI API 연결됨")
            except Exception as e:
                print(f"OpenAI 초기화 실패: {e}")
    
    def research_topic(self, keywords: str, direction: str, web_research_data: str = None) -> dict:
        """키워드와 방향성을 기반으로 콘텐츠 리서치"""
        
        if not self.llm:
            # API 키가 없으면 기본 리서치 데이터 반환
            return {
                "raw_research": f"키워드: {keywords}\n방향성: {direction}\n\n웹 리서치:\n{web_research_data or '검색 결과 없음'}",
                "keywords": keywords,
                "direction": direction
            }
        
        # 웹 리서치 데이터 포함
        research_context = f"""키워드: {keywords}
방향성: {direction}

웹 검색 정보:
{web_research_data or '추가 검색 정보 없음'}
"""
        
        from langchain_core.prompts import ChatPromptTemplate
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 B2B 보안 마케팅 전문가입니다. 
            주어진 키워드, 방향성, 그리고 웹 검색 결과를 바탕으로 트렌디하고 매력적인 콘텐츠 아이디어를 제공하세요."""),
            ("user", """{research_context}

다음 정보를 분석하여 제공하세요:
1. 핵심 메시지 (key_message)
2. 타겟 독자 (target_audience)
3. 주요 포인트 3가지 (main_points)
4. 추천 해시태그 (hashtags)
5. 콘텐츠 톤 (tone)
6. 웹 검색 결과에서 발견한 최신 트렌드나 인사이트""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "research_context": research_context
        })
        
        return {
            "raw_research": response.content,
            "keywords": keywords,
            "direction": direction,
            "web_data": web_research_data,
            "api_provider": self.api_provider
        }
