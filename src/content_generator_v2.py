"""고급 콘텐츠 생성 모듈"""
import os

class AdvancedContentGenerator:
    def __init__(self):
        # OpenAI 또는 Gemini 선택
        self.api_provider = None
        self.llm = None
        
        gemini_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if gemini_key:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                self.llm = ChatGoogleGenerativeAI(
                    model="models/gemini-1.5-flash-latest",
                    temperature=0.8,
                    google_api_key=gemini_key,
                    convert_system_message_to_human=True
                )
                self.api_provider = "gemini"
            except Exception as e:
                print(f"Gemini 초기화 실패: {e}")
        
        if not self.llm and openai_key:
            try:
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0.8,
                    api_key=openai_key
                )
                self.api_provider = "openai"
            except Exception as e:
                print(f"OpenAI 초기화 실패: {e}")
    
    def generate_by_template(self, template: str, research_data: dict, config: dict, variant: int = 0) -> dict:
        """템플릿에 따라 콘텐츠 생성"""
        
        if not self.llm:
            return {}
        
        # 공통 프롬프트 요소
        base_context = f"""
키워드: {config['keywords']}
설명: {config['description']}
타겟: {config['audience']}
산업: {config.get('industry', '일반')}
톤: {config['tone']}
길이: {config['length']}
브랜드: {config.get('brand_name', 'MarkAny')}
브랜드 가치: {config.get('brand_values', '혁신, 신뢰')}
CTA 포함: {config.get('include_cta', True)}
SEO 최적화: {config.get('include_seo', True)}
버전: {variant + 1}
"""
        
        # 레퍼런스 정보 추가
        if config.get('reference_data'):
            ref_data = config['reference_data']
            base_context += f"""

레퍼런스 학습:
- 소스: {ref_data['source']}
- 스타일 분석: {ref_data['analysis'].get('analysis', '분석 정보 없음')}
- 참고 텍스트 샘플: {ref_data['text'][:300]}...

위 레퍼런스의 톤, 문체, 구조를 참고하여 유사한 스타일로 작성하세요.
"""
        
        if template == "blog_post":
            return self._generate_blog_post(base_context, research_data)
        elif template == "twitter_thread":
            return self._generate_twitter_thread(base_context, research_data)
        elif template == "linkedin_post":
            return self._generate_linkedin_post(base_context, research_data)
        elif template == "marketing_email":
            return self._generate_marketing_email(base_context, research_data)
        else:
            return self._generate_generic_content(base_context, research_data, template)
    
    def _generate_blog_post(self, context: str, research: dict) -> dict:
        """블로그 포스트 생성"""
        
        from langchain_core.prompts import ChatPromptTemplate
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 B2B 마케팅 콘텐츠 전문가입니다.
            SEO 최적화되고 독자를 사로잡는 블로그 포스트를 작성하세요."""),
            ("user", """{context}

리서치 데이터:
{research}

다음 형식으로 블로그 포스트를 작성하세요:
- 매력적인 제목 (클릭을 유도)
- 도입부 (문제 제기)
- 본문 (3-5개 섹션, 각 섹션에 소제목)
- 실용적인 팁과 예시
- 결론 및 CTA
- SEO 키워드 자연스럽게 포함""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "context": context,
            "research": research["raw_research"]
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
    
    def _generate_twitter_thread(self, context: str, research: dict) -> dict:
        """트위터 스레드 생성"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 소셜 미디어 마케팅 전문가입니다.
            바이럴되기 쉬운 임팩트 있는 트위터 스레드를 작성하세요."""),
            ("user", """{context}

리서치 데이터:
{research}

트위터 스레드를 작성하세요:
- 첫 트윗: 강력한 훅 (호기심 유발)
- 3-5개 후속 트윗 (각 280자 이내)
- 이모지 적절히 활용
- 해시태그 2-3개
- 마지막 트윗에 CTA
- 각 트윗을 [TWEET 1], [TWEET 2] 형식으로 구분""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "context": context,
            "research": research["raw_research"]
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
            "posts": tweets,
            "platform": "twitter"
        }
    
    def _generate_linkedin_post(self, context: str, research: dict) -> dict:
        """LinkedIn 포스트 생성"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 B2B 소셜 미디어 전문가입니다.
            전문성과 인사이트가 돋보이는 LinkedIn 포스트를 작성하세요."""),
            ("user", """{context}

리서치 데이터:
{research}

LinkedIn 포스트를 작성하세요:
- 전문적이면서도 개인적인 톤
- 인사이트와 경험 공유
- 구체적인 예시나 데이터
- 질문으로 참여 유도
- 관련 해시태그 3-5개""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "context": context,
            "research": research["raw_research"]
        })
        
        return {
            "content": response.content,
            "platform": "linkedin"
        }
    
    def _generate_marketing_email(self, context: str, research: dict) -> dict:
        """마케팅 이메일 생성"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 이메일 마케팅 전문가입니다.
            높은 오픈율과 클릭률을 달성하는 이메일을 작성하세요."""),
            ("user", """{context}

리서치 데이터:
{research}

마케팅 이메일을 작성하세요:
- 제목: 호기심을 자극하는 제목 (50자 이내)
- 프리헤더: 제목을 보완하는 텍스트
- 본문: 개인화된 인사, 가치 제안, 혜택, CTA
- 모바일 친화적인 짧은 문단
- 명확한 CTA 버튼 텍스트""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "context": context,
            "research": research["raw_research"]
        })
        
        content = response.content
        lines = content.split('\n')
        
        # 제목 추출
        subject = ""
        for line in lines:
            if '제목:' in line or 'Subject:' in line:
                subject = line.split(':', 1)[1].strip()
                break
        
        return {
            "subject": subject or "특별한 소식을 전해드립니다",
            "content": content,
            "platform": "email"
        }
    
    def _generate_generic_content(self, context: str, research: dict, template: str) -> dict:
        """일반 콘텐츠 생성"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""당신은 마케팅 콘텐츠 전문가입니다.
            {template} 형식의 콘텐츠를 작성하세요."""),
            ("user", """{context}

리서치 데이터:
{research}

요청된 형식에 맞는 콘텐츠를 작성하세요.""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "context": context,
            "research": research["raw_research"]
        })
        
        return {
            "content": response.content,
            "platform": template
        }
