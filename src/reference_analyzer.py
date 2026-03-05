"""레퍼런스 콘텐츠 분석 모듈"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
import requests
from bs4 import BeautifulSoup

class ReferenceAnalyzer:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.3,
                api_key=api_key
            )
        else:
            self.llm = None
    
    def fetch_content_from_url(self, url: str) -> str:
        """URL에서 콘텐츠 추출"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 불필요한 태그 제거
            for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                tag.decompose()
            
            # 본문 추출 (일반적인 블로그 구조)
            content = ""
            
            # article 태그 우선
            article = soup.find('article')
            if article:
                content = article.get_text(separator='\n', strip=True)
            else:
                # main 태그
                main = soup.find('main')
                if main:
                    content = main.get_text(separator='\n', strip=True)
                else:
                    # body 전체
                    content = soup.get_text(separator='\n', strip=True)
            
            # 길이 제한 (처음 2000자)
            return content[:2000] if content else ""
            
        except Exception as e:
            print(f"URL 콘텐츠 추출 실패: {e}")
            return ""
    
    def analyze_style(self, reference_text: str) -> dict:
        """레퍼런스 콘텐츠의 스타일 분석"""
        
        if not self.llm or not reference_text:
            return {
                "tone": "전문적",
                "style_notes": "레퍼런스 분석 불가",
                "key_phrases": [],
                "structure": "일반적인 구조"
            }
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 콘텐츠 스타일 분석 전문가입니다.
            주어진 텍스트의 톤, 문체, 구조적 특징을 분석하세요."""),
            ("user", """다음 콘텐츠를 분석하세요:

{reference_text}

다음 항목을 분석하여 JSON 형식으로 제공하세요:
1. tone: 전반적인 톤 (전문적, 친근한, 유머러스 등)
2. writing_style: 문체 특징 (간결함, 상세함, 스토리텔링 등)
3. sentence_length: 문장 길이 (짧음, 보통, 김)
4. key_phrases: 자주 사용되는 표현이나 단어 (5개)
5. structure: 콘텐츠 구조 특징
6. emoji_usage: 이모지 사용 여부 및 빈도
7. cta_style: CTA 스타일 (있다면)""")
        ])
        
        try:
            chain = prompt | self.llm
            response = chain.invoke({"reference_text": reference_text})
            
            # 간단한 파싱 (실제로는 JSON 파싱 필요)
            return {
                "analysis": response.content,
                "reference_text": reference_text[:500]  # 일부만 저장
            }
        except Exception as e:
            print(f"스타일 분석 실패: {e}")
            return {
                "tone": "전문적",
                "style_notes": "분석 실패",
                "key_phrases": [],
                "structure": "일반적인 구조"
            }
    
    def get_reference_data(self, config: dict) -> dict:
        """설정에서 레퍼런스 데이터 추출 및 분석"""
        
        if not config.get('use_reference'):
            return None
        
        reference_text = ""
        
        # URL에서 추출
        if config.get('reference_url'):
            reference_text = self.fetch_content_from_url(config['reference_url'])
        
        # 직접 입력
        elif config.get('reference_text'):
            reference_text = config['reference_text']
        
        if not reference_text:
            return None
        
        # 스타일 분석
        analysis = self.analyze_style(reference_text)
        
        return {
            "source": config.get('reference_source', 'unknown'),
            "text": reference_text,
            "analysis": analysis
        }
