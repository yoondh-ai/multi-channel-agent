"""Streamlit 웹 인터페이스"""
import streamlit as st
from dotenv import load_dotenv
import os
from src.agent import MultiChannelAgent

# 환경 변수 로드
load_dotenv()

st.set_page_config(
    page_title="멀티채널 자동 포스팅 에이전트",
    page_icon="🚀",
    layout="wide"
)

# 세션 상태 초기화
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = None
if 'research_data' not in st.session_state:
    st.session_state.research_data = None
if 'selected_channels' not in st.session_state:
    st.session_state.selected_channels = []

st.title("🚀 멀티채널 자동 포스팅 에이전트")
st.markdown("**보안 기술을 트렌디한 콘텐츠로 변환하여 자동 포스팅**")

# 사이드바 - API 설정 확인
with st.sidebar:
    st.header("⚙️ 설정")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    twitter_key = os.getenv("TWITTER_API_KEY")
    medium_token = os.getenv("MEDIUM_ACCESS_TOKEN")
    
    st.write("API 연결 상태:")
    st.write(f"✅ OpenAI: {'설정됨' if openai_key else '❌ 미설정'}")
    st.write(f"{'✅' if twitter_key else '❌'} Twitter: {'설정됨' if twitter_key else '미설정'}")
    st.write(f"{'✅' if medium_token else '❌'} Medium: {'설정됨' if medium_token else '미설정'}")
    
    st.markdown("---")
    st.markdown("`.env` 파일에 API 키를 설정하세요")

# 메인 입력 폼
col1, col2 = st.columns([2, 1])

with col1:
    keywords = st.text_input(
        "🔑 키워드",
        placeholder="예: 제로트러스트, 랜섬웨어 방어, 클라우드 보안",
        help="콘텐츠의 핵심 키워드를 입력하세요"
    )
    
    direction = st.text_area(
        "🎯 작성 방향",
        placeholder="예: 중소기업 IT 담당자를 위한 실용적인 가이드, 최신 트렌드 중심, 쉽고 친근한 톤",
        help="콘텐츠의 방향성과 톤을 설명하세요",
        height=100
    )

with col2:
    st.write("📢 포스팅 채널")
    post_to_blog = st.checkbox("블로그 (Medium)", value=True)
    post_to_twitter = st.checkbox("트위터 (X)", value=True)

# 1단계: 콘텐츠 생성 버튼
if st.button("🎨 콘텐츠 생성", type="primary", use_container_width=True):
    if not keywords or not direction:
        st.error("키워드와 작성 방향을 모두 입력해주세요")
    else:
        channels = []
        if post_to_blog:
            channels.append("blog")
        if post_to_twitter:
            channels.append("twitter")
        
        if not channels:
            st.warning("최소 하나의 채널을 선택하세요")
        else:
            # API 키 확인 및 모드 결정
            use_mock = not openai_key
            
            if use_mock:
                st.info("ℹ️ 데모 모드: OpenAI API 키가 없어 샘플 콘텐츠를 생성합니다.")
            
            with st.spinner("🤖 AI 에이전트가 콘텐츠를 생성하고 있습니다..."):
                try:
                    agent = MultiChannelAgent()
                    results = agent.create_content_only(keywords, direction, channels, use_mock=use_mock)
                    
                    # 세션 상태에 저장
                    st.session_state.generated_content = results["content"]
                    st.session_state.research_data = results["research"]
                    st.session_state.selected_channels = channels
                    
                    st.success("✅ 콘텐츠 생성 완료! 아래에서 검수 후 포스팅하세요.")
                    st.rerun()
                
                except Exception as e:
                    st.error(f"오류 발생: {str(e)}")
                    st.exception(e)

# 2단계: 생성된 콘텐츠 표시 및 검수
if st.session_state.generated_content:
    st.markdown("---")
    st.header("📊 생성된 콘텐츠 (검수)")
    
    # 리서치 결과
    with st.expander("🔍 리서치 결과", expanded=False):
        st.write(st.session_state.research_data["raw_research"])
    
    # 블로그 콘텐츠
    if "blog" in st.session_state.generated_content:
        st.subheader("📝 블로그 포스트")
        
        # 편집 가능한 제목
        edited_blog_title = st.text_input(
            "제목",
            value=st.session_state.generated_content["blog"]["title"],
            key="blog_title_edit"
        )
        
        # 편집 가능한 본문
        edited_blog_content = st.text_area(
            "본문",
            value=st.session_state.generated_content["blog"]["content"],
            height=400,
            key="blog_content_edit"
        )
        
        # 수정사항 저장
        st.session_state.generated_content["blog"]["title"] = edited_blog_title
        st.session_state.generated_content["blog"]["content"] = edited_blog_content
    
    # 트위터 콘텐츠
    if "twitter" in st.session_state.generated_content:
        st.subheader("🐦 트위터 스레드")
        
        edited_tweets = []
        for i, tweet in enumerate(st.session_state.generated_content["twitter"]["tweets"], 1):
            edited_tweet = st.text_area(
                f"트윗 {i}",
                value=tweet,
                height=100,
                key=f"tweet_edit_{i}"
            )
            edited_tweets.append(edited_tweet)
        
        # 수정사항 저장
        st.session_state.generated_content["twitter"]["tweets"] = edited_tweets
    
    # 3단계: 포스팅 버튼
    st.markdown("---")
    col_post1, col_post2, col_post3 = st.columns([1, 1, 1])
    
    with col_post1:
        if st.button("✅ 검수 완료 - 포스팅 실행", type="primary", use_container_width=True):
            with st.spinner("📤 포스팅 중..."):
                try:
                    agent = MultiChannelAgent()
                    post_results = agent.post_content(
                        st.session_state.generated_content,
                        st.session_state.selected_channels
                    )
                    
                    st.success("🎉 포스팅 완료!")
                    
                    # 포스팅 결과 표시
                    for channel, result in post_results.items():
                        if result["success"]:
                            st.success(f"{channel}: {result['message']}")
                        else:
                            st.info(f"{channel}: {result['message']}")
                    
                except Exception as e:
                    st.error(f"포스팅 오류: {str(e)}")
    
    with col_post2:
        if st.button("🔄 다시 생성", use_container_width=True):
            st.session_state.generated_content = None
            st.session_state.research_data = None
            st.session_state.selected_channels = []
            st.rerun()
    
    with col_post3:
        if st.button("❌ 취소", use_container_width=True):
            st.session_state.generated_content = None
            st.session_state.research_data = None
            st.session_state.selected_channels = []
            st.rerun()

# 사용 가이드
with st.expander("📖 사용 가이드"):
    st.markdown("""
    ### 시작하기
    1. `.env` 파일에 API 키 설정
    2. 키워드와 작성 방향 입력
    3. 포스팅할 채널 선택
    4. '콘텐츠 생성 및 포스팅' 버튼 클릭
    
    ### API 키 발급
    - **OpenAI**: https://platform.openai.com/api-keys
    - **Twitter**: https://developer.twitter.com/
    - **Medium**: https://medium.com/me/settings (Integration tokens)
    
    ### 팁
    - 구체적인 키워드일수록 더 정확한 콘텐츠 생성
    - 타겟 독자를 명확히 하면 더 효과적
    - 여러 번 생성해서 최적의 결과 선택
    """)
