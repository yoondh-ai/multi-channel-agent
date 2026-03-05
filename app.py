"""Jasper AI 스타일 마케팅 콘텐츠 생성 플랫폼"""
import streamlit as st
from dotenv import load_dotenv
import os
from datetime import datetime
from src.agent_v2 import MarketingContentAgent
from src.templates import CONTENT_TEMPLATES, TONE_OPTIONS, AUDIENCE_OPTIONS

# 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="AI 마케팅 콘텐츠 생성 플랫폼",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .template-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s;
    }
    .template-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }
    .selected-template {
        border-color: #667eea;
        background: #f8f9ff;
    }
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
    }
    .step {
        flex: 1;
        text-align: center;
        padding: 1rem;
        background: #f5f5f5;
        margin: 0 0.5rem;
        border-radius: 8px;
    }
    .step.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .content-preview {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'template' not in st.session_state:
    st.session_state.template = None
if 'generated_contents' not in st.session_state:
    st.session_state.generated_contents = []
if 'history' not in st.session_state:
    st.session_state.history = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# 헤더
st.markdown("""
<div class="main-header">
    <h1>✨ AI 마케팅 콘텐츠 생성 플랫폼</h1>
    <p>보안 기술을 고객의 마음을 사로잡는 마케팅 콘텐츠로 변환</p>
</div>
""", unsafe_allow_html=True)

# 사이드바 - 히스토리 & 설정
with st.sidebar:
    st.header("⚙️ 설정")
    
    # API 상태
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        st.success("✅ AI 엔진 연결됨")
    else:
        st.info("ℹ️ 데모 모드 (샘플 콘텐츠)")
    
    st.markdown("---")
    
    # 브랜드 보이스 설정
    st.subheader("🎨 브랜드 보이스")
    brand_name = st.text_input("브랜드명", value="MarkAny", key="brand_name")
    brand_values = st.text_area(
        "핵심 가치",
        value="혁신, 신뢰, 보안",
        height=80,
        key="brand_values"
    )
    
    st.markdown("---")
    
    # 히스토리
    st.subheader("📚 최근 생성 콘텐츠")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history[-5:])):
            with st.expander(f"{item['template']} - {item['timestamp'][:10]}"):
                st.write(f"**키워드:** {item['keywords']}")
                if st.button("다시 불러오기", key=f"load_{i}"):
                    st.session_state.generated_contents = item['contents']
                    st.rerun()
    else:
        st.write("아직 생성된 콘텐츠가 없습니다")
    
    st.markdown("---")
    
    # 즐겨찾기
    st.subheader("⭐ 즐겨찾기")
    if st.session_state.favorites:
        st.write(f"{len(st.session_state.favorites)}개 저장됨")
    else:
        st.write("즐겨찾기가 비어있습니다")

# 메인 컨텐츠
# 단계 표시
steps = ["템플릿 선택", "콘텐츠 설정", "생성 & 검수", "포스팅"]
cols = st.columns(4)
for i, (col, step_name) in enumerate(zip(cols, steps), 1):
    with col:
        if i == st.session_state.step:
            st.markdown(f"**🔵 {i}. {step_name}**")
        elif i < st.session_state.step:
            st.markdown(f"✅ {i}. {step_name}")
        else:
            st.markdown(f"⚪ {i}. {step_name}")

st.markdown("---")

# Step 1: 템플릿 선택
if st.session_state.step == 1:
    st.header("1️⃣ 콘텐츠 템플릿 선택")
    st.write("생성하고 싶은 마케팅 콘텐츠 유형을 선택하세요")
    
    # 템플릿 카테고리
    tab1, tab2, tab3, tab4 = st.tabs(["📝 블로그 & 아티클", "📱 소셜 미디어", "📧 이메일", "🎯 광고"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📄 블로그 포스트", use_container_width=True, key="blog"):
                st.session_state.template = "blog_post"
                st.session_state.step = 2
                st.rerun()
            st.caption("긴 형식의 SEO 최적화 블로그")
            
            if st.button("📰 보도자료", use_container_width=True, key="press"):
                st.session_state.template = "press_release"
                st.session_state.step = 2
                st.rerun()
            st.caption("공식 발표용 보도자료")
        
        with col2:
            if st.button("📚 케이스 스터디", use_container_width=True, key="case"):
                st.session_state.template = "case_study"
                st.session_state.step = 2
                st.rerun()
            st.caption("고객 성공 사례")
            
            if st.button("📖 백서", use_container_width=True, key="whitepaper"):
                st.session_state.template = "whitepaper"
                st.session_state.step = 2
                st.rerun()
            st.caption("전문적인 기술 문서")
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🐦 트위터 스레드", use_container_width=True, key="twitter"):
                st.session_state.template = "twitter_thread"
                st.session_state.step = 2
                st.rerun()
            st.caption("임팩트 있는 트윗 시리즈")
            
            if st.button("💼 LinkedIn 포스트", use_container_width=True, key="linkedin"):
                st.session_state.template = "linkedin_post"
                st.session_state.step = 2
                st.rerun()
            st.caption("B2B 전문가 네트워크용")
        
        with col2:
            if st.button("📸 Instagram 캡션", use_container_width=True, key="instagram"):
                st.session_state.template = "instagram_caption"
                st.session_state.step = 2
                st.rerun()
            st.caption("시각적 콘텐츠용 캡션")
            
            if st.button("🎬 카드뉴스", use_container_width=True, key="cardnews"):
                st.session_state.template = "card_news"
                st.session_state.step = 2
                st.rerun()
            st.caption("슬라이드 형식 콘텐츠")
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📧 마케팅 이메일", use_container_width=True, key="email"):
                st.session_state.template = "marketing_email"
                st.session_state.step = 2
                st.rerun()
            st.caption("뉴스레터 & 프로모션")
            
        with col2:
            if st.button("🎁 제품 출시 이메일", use_container_width=True, key="launch"):
                st.session_state.template = "product_launch"
                st.session_state.step = 2
                st.rerun()
            st.caption("신제품 런칭 공지")
    
    with tab4:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎯 Google 광고", use_container_width=True, key="google"):
                st.session_state.template = "google_ads"
                st.session_state.step = 2
                st.rerun()
            st.caption("검색 광고 카피")
            
        with col2:
            if st.button("📱 소셜 미디어 광고", use_container_width=True, key="social_ads"):
                st.session_state.template = "social_ads"
                st.session_state.step = 2
                st.rerun()
            st.caption("Facebook, Instagram 광고")

# Step 2: 콘텐츠 설정
elif st.session_state.step == 2:
    st.header(f"2️⃣ 콘텐츠 설정: {CONTENT_TEMPLATES[st.session_state.template]['name']}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 기본 정보
        st.subheader("📝 기본 정보")
        keywords = st.text_input(
            "핵심 키워드",
            placeholder="예: 제로트러스트, 랜섬웨어 방어, 클라우드 보안",
            help="콘텐츠의 주제가 되는 키워드를 입력하세요"
        )
        
        description = st.text_area(
            "상세 설명",
            placeholder="어떤 내용을 다루고 싶으신가요? 구체적으로 작성할수록 더 정확한 콘텐츠가 생성됩니다.",
            height=120
        )
        
        # 타겟 오디언스
        st.subheader("🎯 타겟 오디언스")
        col_a, col_b = st.columns(2)
        with col_a:
            audience = st.selectbox("대상", list(AUDIENCE_OPTIONS.keys()))
        with col_b:
            industry = st.text_input("산업/분야", placeholder="예: IT, 금융, 제조")
        
        # 톤앤매너
        st.subheader("🎨 톤앤매너")
        tone = st.select_slider(
            "콘텐츠 톤",
            options=list(TONE_OPTIONS.keys()),
            value="전문적"
        )
        st.caption(TONE_OPTIONS[tone])
        
        # 추가 옵션
        st.subheader("⚙️ 추가 옵션")
        col_c, col_d = st.columns(2)
        with col_c:
            length = st.select_slider(
                "콘텐츠 길이",
                options=["짧게", "보통", "길게"],
                value="보통"
            )
        with col_d:
            variants = st.number_input(
                "생성 개수",
                min_value=1,
                max_value=5,
                value=3,
                help="여러 버전을 생성하여 최적의 콘텐츠를 선택하세요"
            )
        
        include_cta = st.checkbox("CTA(Call-to-Action) 포함", value=True)
        include_seo = st.checkbox("SEO 키워드 최적화", value=True)
    
    with col2:
        st.subheader("📋 템플릿 정보")
        template_info = CONTENT_TEMPLATES[st.session_state.template]
        st.info(f"**{template_info['name']}**\n\n{template_info['description']}")
        
        st.markdown("**특징:**")
        for feature in template_info['features']:
            st.markdown(f"• {feature}")
        
        st.markdown("**권장 길이:**")
        st.write(template_info['recommended_length'])
    
    # 버튼
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        if st.button("⬅️ 이전", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    with col_btn2:
        if st.button("✨ 콘텐츠 생성", type="primary", use_container_width=True):
            if not keywords:
                st.error("핵심 키워드를 입력해주세요")
            else:
                # 설정 저장
                st.session_state.content_config = {
                    "keywords": keywords,
                    "description": description,
                    "audience": audience,
                    "industry": industry,
                    "tone": tone,
                    "length": length,
                    "variants": variants,
                    "include_cta": include_cta,
                    "include_seo": include_seo,
                    "brand_name": brand_name,
                    "brand_values": brand_values
                }
                st.session_state.step = 3
                st.rerun()

# Step 3: 생성 & 검수
elif st.session_state.step == 3:
    st.header("3️⃣ 콘텐츠 생성 & 검수")
    
    # 콘텐츠 생성
    if not st.session_state.generated_contents:
        with st.spinner("🤖 AI가 콘텐츠를 생성하고 있습니다..."):
            try:
                agent = MarketingContentAgent()
                config = st.session_state.content_config
                
                contents = agent.generate_content(
                    template=st.session_state.template,
                    config=config,
                    use_mock=not os.getenv("OPENAI_API_KEY")
                )
                
                st.session_state.generated_contents = contents
                
                # 히스토리에 추가
                st.session_state.history.append({
                    "template": CONTENT_TEMPLATES[st.session_state.template]['name'],
                    "keywords": config['keywords'],
                    "contents": contents,
                    "timestamp": datetime.now().isoformat()
                })
                
                st.success(f"✅ {len(contents)}개의 콘텐츠 버전이 생성되었습니다!")
                st.rerun()
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
                st.exception(e)
    
    # 생성된 콘텐츠 표시
    if st.session_state.generated_contents:
        # 버전 선택 탭
        tabs = st.tabs([f"버전 {i+1}" for i in range(len(st.session_state.generated_contents))])
        
        for i, (tab, content) in enumerate(zip(tabs, st.session_state.generated_contents)):
            with tab:
                col_main, col_side = st.columns([3, 1])
                
                with col_main:
                    # 제목 편집
                    if 'title' in content:
                        edited_title = st.text_input(
                            "제목",
                            value=content['title'],
                            key=f"title_{i}"
                        )
                        content['title'] = edited_title
                    
                    # 본문 편집
                    if 'content' in content:
                        edited_content = st.text_area(
                            "본문",
                            value=content['content'],
                            height=400,
                            key=f"content_{i}"
                        )
                        content['content'] = edited_content
                    
                    # 트윗/포스트 편집
                    if 'posts' in content:
                        for j, post in enumerate(content['posts']):
                            edited_post = st.text_area(
                                f"포스트 {j+1}",
                                value=post,
                                height=100,
                                key=f"post_{i}_{j}"
                            )
                            content['posts'][j] = edited_post
                
                with col_side:
                    st.subheader("📊 분석")
                    
                    # 글자 수
                    if 'content' in content:
                        char_count = len(content['content'])
                        st.metric("글자 수", f"{char_count:,}")
                    
                    # SEO 점수 (모의)
                    if st.session_state.content_config.get('include_seo'):
                        seo_score = 85
                        st.metric("SEO 점수", f"{seo_score}/100")
                    
                    # 가독성
                    readability = "높음"
                    st.metric("가독성", readability)
                    
                    st.markdown("---")
                    
                    # 액션 버튼
                    if st.button("⭐ 즐겨찾기", key=f"fav_{i}", use_container_width=True):
                        st.session_state.favorites.append(content)
                        st.success("즐겨찾기에 추가됨!")
                    
                    if st.button("📋 복사", key=f"copy_{i}", use_container_width=True):
                        st.info("클립보드에 복사됨!")
                    
                    if st.button("💾 다운로드", key=f"download_{i}", use_container_width=True):
                        st.download_button(
                            "TXT 다운로드",
                            data=content.get('content', ''),
                            file_name=f"content_{i+1}.txt",
                            key=f"dl_btn_{i}"
                        )
        
        # 하단 버튼
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("⬅️ 이전", use_container_width=True):
                st.session_state.step = 2
                st.rerun()
        
        with col2:
            if st.button("🔄 다시 생성", use_container_width=True):
                st.session_state.generated_contents = []
                st.rerun()
        
        with col3:
            if st.button("❌ 취소", use_container_width=True):
                st.session_state.step = 1
                st.session_state.generated_contents = []
                st.rerun()
        
        with col4:
            if st.button("✅ 포스팅 준비", type="primary", use_container_width=True):
                st.session_state.step = 4
                st.rerun()

# Step 4: 포스팅
elif st.session_state.step == 4:
    st.header("4️⃣ 포스팅")
    
    st.info("🚀 선택한 콘텐츠를 각 채널에 포스팅할 준비가 되었습니다.")
    
    # 채널 선택
    st.subheader("📢 포스팅 채널 선택")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        post_blog = st.checkbox("📝 블로그 (Medium)", value=True)
    with col2:
        post_twitter = st.checkbox("🐦 트위터", value=True)
    with col3:
        post_linkedin = st.checkbox("💼 LinkedIn", value=False)
    
    # 예약 포스팅
    st.subheader("⏰ 예약 설정")
    schedule_post = st.checkbox("예약 포스팅")
    
    if schedule_post:
        col_date, col_time = st.columns(2)
        with col_date:
            post_date = st.date_input("날짜")
        with col_time:
            post_time = st.time_input("시간")
    
    st.markdown("---")
    
    # 버튼
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("⬅️ 이전", use_container_width=True):
            st.session_state.step = 3
            st.rerun()
    
    with col2:
        if st.button("🚀 포스팅 실행", type="primary", use_container_width=True):
            with st.spinner("📤 포스팅 중..."):
                # 포스팅 로직 (데모)
                import time
                time.sleep(2)
                
                st.success("🎉 포스팅 완료!")
                
                # 결과 표시
                if post_blog:
                    st.success("✅ 블로그: 포스팅 완료 (미리보기 모드)")
                if post_twitter:
                    st.success("✅ 트위터: 포스팅 완료 (미리보기 모드)")
                if post_linkedin:
                    st.success("✅ LinkedIn: 포스팅 완료 (미리보기 모드)")
                
                if st.button("🏠 처음으로"):
                    st.session_state.step = 1
                    st.session_state.generated_contents = []
                    st.rerun()
