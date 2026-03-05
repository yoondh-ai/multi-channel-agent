"""웹 검색 및 정보 수집 모듈"""
import os
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

class WebResearcher:
    def __init__(self):
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
    
    def search_web(self, query: str, num_results: int = 5) -> List[Dict]:
        """웹 검색 수행"""
        
        # Serper API 사용 (Google Search API)
        if self.serper_api_key:
            return self._search_with_serper(query, num_results)
        # Tavily API 사용
        elif self.tavily_api_key:
            return self._search_with_tavily(query, num_results)
        # API 없으면 기본 검색
        else:
            return self._basic_search(query, num_results)
    
    def _search_with_serper(self, query: str, num_results: int) -> List[Dict]:
        """Serper API로 검색"""
        try:
            url = "https://google.serper.dev/search"
            headers = {
                'X-API-KEY': self.serper_api_key,
                'Content-Type': 'application/json'
            }
            payload = {
                'q': query,
                'num': num_results
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get('organic', [])[:num_results]:
                results.append({
                    'title': item.get('title', ''),
                    'snippet': item.get('snippet', ''),
                    'link': item.get('link', ''),
                    'source': 'serper'
                })
            
            return results
            
        except Exception as e:
            print(f"Serper 검색 실패: {e}")
            return []
    
    def _search_with_tavily(self, query: str, num_results: int) -> List[Dict]:
        """Tavily API로 검색"""
        try:
            url = "https://api.tavily.com/search"
            headers = {
                'Content-Type': 'application/json'
            }
            payload = {
                'api_key': self.tavily_api_key,
                'query': query,
                'max_results': num_results
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get('results', [])[:num_results]:
                results.append({
                    'title': item.get('title', ''),
                    'snippet': item.get('content', ''),
                    'link': item.get('url', ''),
                    'source': 'tavily'
                })
            
            return results
            
        except Exception as e:
            print(f"Tavily 검색 실패: {e}")
            return []
    
    def _basic_search(self, query: str, num_results: int) -> List[Dict]:
        """기본 검색 (DuckDuckGo HTML 파싱)"""
        try:
            # DuckDuckGo HTML 검색
            url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            # 검색 결과 파싱
            for result in soup.find_all('div', class_='result')[:num_results]:
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')
                
                if title_elem:
                    results.append({
                        'title': title_elem.get_text(strip=True),
                        'snippet': snippet_elem.get_text(strip=True) if snippet_elem else '',
                        'link': title_elem.get('href', ''),
                        'source': 'duckduckgo'
                    })
            
            return results
            
        except Exception as e:
            print(f"기본 검색 실패: {e}")
            return []
    
    def fetch_page_content(self, url: str, max_length: int = 2000) -> str:
        """웹페이지 콘텐츠 추출"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 불필요한 태그 제거
            for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                tag.decompose()
            
            # 본문 추출
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
                    body = soup.find('body')
                    if body:
                        content = body.get_text(separator='\n', strip=True)
            
            # 길이 제한
            return content[:max_length] if content else ""
            
        except Exception as e:
            print(f"페이지 콘텐츠 추출 실패: {e}")
            return ""
    
    def research_topic(self, keywords: str, description: str, industry: str = "") -> Dict:
        """주제에 대한 종합 리서치"""
        
        # 검색 쿼리 생성
        search_queries = [
            f"{keywords} {industry} 최신 트렌드",
            f"{keywords} 사례 연구",
            f"{keywords} 가이드",
        ]
        
        all_results = []
        
        # 각 쿼리로 검색
        for query in search_queries[:2]:  # 처음 2개만 사용
            results = self.search_web(query, num_results=3)
            all_results.extend(results)
        
        # 검색 결과 요약
        research_summary = {
            'keywords': keywords,
            'description': description,
            'industry': industry,
            'search_results': all_results,
            'total_sources': len(all_results)
        }
        
        # 상위 결과의 콘텐츠 추출 (선택적)
        if all_results:
            top_result = all_results[0]
            if top_result.get('link'):
                content = self.fetch_page_content(top_result['link'], max_length=1000)
                research_summary['top_content'] = content
        
        return research_summary
    
    def format_research_for_prompt(self, research_data: Dict) -> str:
        """리서치 데이터를 프롬프트용 텍스트로 변환"""
        
        formatted = f"""
키워드: {research_data['keywords']}
산업: {research_data.get('industry', '일반')}

웹 검색 결과 ({research_data['total_sources']}개 소스):

"""
        
        for i, result in enumerate(research_data['search_results'][:5], 1):
            formatted += f"""
{i}. {result['title']}
   {result['snippet']}
   출처: {result['link']}

"""
        
        if research_data.get('top_content'):
            formatted += f"""
주요 콘텐츠 발췌:
{research_data['top_content'][:500]}...
"""
        
        return formatted
