"""Jasper AI 스타일 마케팅 콘텐츠 생성 플랫폼"""
import streamlit as st
from dotenv import load_dotenv
import os
from datetime import datetime
from src.agent_v2 import MarketingContentAgent
from src.templates import MARKETING_FRAMEWORKS, CONTENT_TEMPLATES, TONE_OPTIONS, AUDIENCE_OPTIONS

# 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="AI 마케팅 콘텐츠 생성",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Jasper 스타일 CSS
st.markdown("""
<style>
    /* 전체 배경 */
    .main {
        background-color: #f8f9fa;
    }
    
    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #6366f1 0%, #8b5cf6 100%);
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600;
    }
    
    /* 메인 헤더 */
    .main-header {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-header h1 {
        color: #1f2937;
        margin: 0;
        font-size: 2.5rem;
    }
    
    .main-header p {
        color: #6b7280;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    /* 입력 폼 카드 */
    .input-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    /* 결과 카드 */
    .result-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        min-height: 500px;
    }
    
    /* 버튼 스타일 */
    .stButton button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f3f4f6;
        padding: 0.5rem;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 6px;
        color: #6b7280;
        font-weight: 600;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
    }
    
    /* 텍스트 영역 */
    .stTextArea textarea {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        font-size: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* 메트릭 카드 */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        color: #6366f1;
        font-weight: 700;
    }
    
    /* API 상태 */
    .api-status {
        background: #ecfdf5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .api-warning {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    /* 섹션 제목 */
    .section-title {
        color: #1f2937;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
    }
    
    /* 편집기 툴바 */
    .editor-toolbar {
        background: #f3f4f6;
        padding: 0.75rem;
        border-radius: 8px 8px 0 0;
        display: flex;
        gap: 0.5rem;
        margin-bottom: -1rem;
    }
    
    /* 채널 아이콘 */
    .channel-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'generated_contents' not in st.session_state:
    st.session_state.generated_contents = {}
if 'current_framework' not in st.session_state:
    st.session_state.current_framework = None
if 'current_audience' not in st.session_state:
    st.session_state.current_audience = None
if 'current_tone' not in st.session_state:
    st.session_state.current_tone = None

# API 상태 확인
groq_key = os.getenv("GROQ_API_KEY")
gemini_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

api_available = bool(groq_key or gemini_key or openai_key)
api_provider = None
if groq_key:
    api_provider = "Groq (무료)"
elif gemini_key:
    api_provider = "Gemini"
elif openai_key:
    api_provider = "OpenAI"

# ========== 사이드바: 템플릿 선택 ==========
with st.sidebar:
    st.markdown("### ✨ 콘텐츠 설정")
    
    st.markdown("---")
    
    # 마케팅 프레임워크 선택
    st.markdown("#### 📋 마케팅 프레임워크")
    framework_options = {k: v["name"] for k, v in MARKETING_FRAMEWORKS.items()}
    selected_framework = st.selectbox(
        "프레임워크",
        options=list(framework_options.keys()),
        format_func=lambda x: framework_options[x],
        label_visibility="collapsed"
    )
    
    if selected_framework:
        framework_info = MARKETING_FRAMEWORKS[selected_framework]
        st.caption(f"💡 {framework_info['description']}")
        st.caption(f"✅ {framework_info['best_for']}")
        st.session_state.current_framework = selected_framework
    
    st.markdown("---")
    
    # 타겟 독자
    st.markdown("#### 🎯 타겟 독자")
    selected_audience = st.selectbox(
        "독자",
        options=list(AUDIENCE_OPTIONS.keys()),
        label_visibility="collapsed"
    )
    st.caption(AUDIENCE_OPTIONS[selected_audience])
    st.session_state.current_audience = selected_audience
    
    st.markdown("---")
    
    # 말투 (Tone)
    st.markdown("#### 🎨 말투 (Tone)")
    selected_tone = st.selectbox(
        "톤",
        options=list(TONE_OPTIONS.keys()),
        label_visibility="collapsed"
    )
    st.caption(TONE_OPTIONS[selected_tone])
    st.session_state.current_tone = selected_tone
    
    st.markdown("---")
    
    # 생성 옵션
    st.markdown("#### ⚙️ 생성 옵션")
    num_variants = st.slider("생성 개수", 1, 3, 2)
    include_seo = st.checkbox("SEO 최적화", value=True)
    include_cta = st.checkbox("CTA 포함", value=True)
    
    st.markdown("---")
    
    # API 상태
    if api_available:
        st.success(f"✅ {api_provider} 연결됨")
    else:
        st.warning("⚠️ 데모 모드")
        with st.expander("API 설정"):
            st.markdown("""
            **Groq (무료 추천)**
            1. https://console.groq.com
            2. API 키 발급
            3. Secrets에 추가:
            ```
            GROQ_API_KEY = "gsk_..."
            ```
            """)

# ========== 메인 헤더 ==========
st.markdown("""
<div class="main-header">
    <h1>✨ AI 마케팅 콘텐츠 생성</h1>
    <p>Jasper 스타일 - 전문적인 마케팅 콘텐츠를 몇 초 만에</p>
</div>
""", unsafe_allow_html=True)

# ========== 메인 레이아웃: 좌우 2분할 ==========
left_col, right_col = st.columns([1, 1], gap="large")

# ========== 좌측: 입력 폼 ==========
with left_col:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📝 콘텐츠 정보 입력</div>', unsafe_allow_html=True)
    
    # 제품/서비스명
    product_name = st.text_input(
        "제품/서비스명",
        placeholder="예: MarkAny 제로트러스트 솔루션",
        help="마케팅할 제품이나 서비스의 이름을 입력하세요"
    )
    
    # 핵심 특징
    key_features = st.text_area(
        "핵심 특징 (3-5개)",
        placeholder="""예:
• 완벽한 보안 아키텍처
• 클라우드 네이티브 설계
• 실시간 위협 탐지
• 간편한 도입 및 관리
• 24/7 전문가 지원""",
        height=150,
        help="제품의 주요 특징을 나열하세요"
    )
    
    # 타겟 키워드
    keywords = st.text_input(
        "타겟 키워드",
        placeholder="예: 제로트러스트, 클라우드 보안, 네트워크 보안",
        help="SEO를 위한 핵심 키워드를 입력하세요"
    )
    
    # 추가 컨텍스트
    additional_context = st.text_area(
        "추가 정보 (선택사항)",
        placeholder="특별히 강조하고 싶은 내용, 프로모션 정보, 경쟁 우위 등을 입력하세요",
        height=100
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 생성 버튼
    generate_button = st.button("🚀 콘텐츠 생성하기", type="primary", use_container_width=True)
    
    if generate_button:
        if not product_name:
            st.error("❌ 제품/서비스명을 입력하세요")
        elif not key_features:
            st.error("❌ 핵심 특징을 입력하세요")
        else:
            with st.spinner("🤖 AI가 콘텐츠를 생성하고 있습니다..."):
                try:
                    # 설정 구성
                    config = {
                        "keywords": keywords or product_name,
                        "description": f"""
제품명: {product_name}

핵심 특징:
{key_features}

추가 정보:
{additional_context or '없음'}

마케팅 프레임워크: {MARKETING_FRAMEWORKS[selected_framework]['name']}
구조: {' → '.join(MARKETING_FRAMEWORKS[selected_framework]['structure'])}
""",
                        "audience": selected_audience,
                        "tone": selected_tone,
                        "length": "보통 (100-500자)",
                        "variants": num_variants,
                        "include_cta": include_cta,
                        "include_seo": include_seo,
                        "brand_name": product_name.split()[0] if product_name else "MarkAny",
                        "brand_values": "혁신, 신뢰, 보안",
                        "framework": selected_framework
                    }
                    
                    # 에이전트 실행
                    agent = MarketingContentAgent()
                    
                    # 채널별 콘텐츠 생성
                    channels = {
                        "네이버 블로그": "blog_post",
                        "LinkedIn": "linkedin_post",
                        "Twitter": "twitter_thread",
                        "이메일": "marketing_email"
                    }
                    
                    results = {}
                    for channel_name, template in channels.items():
                        contents = agent.generate_content(
                            template=template,
                            config=config,
                            use_mock=(not api_available)
                        )
                        results[channel_name] = contents
                    
                    st.session_state.generated_contents = results
                    
                    if not api_available:
                        st.warning("⚠️ 데모 모드: API 키를 설정하면 실제 AI 콘텐츠를 생성할 수 있습니다")
                    else:
                        st.success(f"✅ 생성 완료! ({api_provider} 사용)")
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ 오류 발생: {str(e)}")
                    st.exception(e)

# ========== 우측: 결과 및 편집기 ==========
with right_col:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    if not st.session_state.generated_contents:
        # 초기 상태
        st.markdown('<div class="section-title">📊 생성 결과</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; color: #9ca3af;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📝</div>
            <h3 style="color: #6b7280;">콘텐츠를 생성해보세요</h3>
            <p>왼쪽에서 정보를 입력하고 생성 버튼을 클릭하세요</p>
            <p style="margin-top: 2rem; font-size: 0.9rem;">
                💡 <strong>팁:</strong> 구체적인 정보를 입력할수록 더 좋은 결과를 얻을 수 있습니다
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # 결과 표시
        st.markdown('<div class="section-title">📊 생성된 콘텐츠</div>', unsafe_allow_html=True)
        
        # 채널별 탭
        channel_icons = {
            "네이버 블로그": "📝",
            "LinkedIn": "💼",
            "Twitter": "🐦",
            "이메일": "📧"
        }
        
        tab_labels = [f"{channel_icons[ch]} {ch}" for ch in st.session_state.generated_contents.keys()]
        tabs = st.tabs(tab_labels)
        
        for tab, (channel_name, contents) in zip(tabs, st.session_state.generated_contents.items()):
            with tab:
                # 버전별 서브탭
                if len(contents) > 1:
                    version_tabs = st.tabs([f"버전 {i+1}" for i in range(len(contents))])
                else:
                    version_tabs = [st.container()]
                
                for ver_idx, (ver_tab, content) in enumerate(zip(version_tabs, contents)):
                    with ver_tab:
                        # 메트릭
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if 'content' in content:
                                char_count = len(content['content'])
                                st.metric("글자 수", f"{char_count}자")
                            elif 'posts' in content:
                                st.metric("포스트", f"{len(content['posts'])}개")
                        with col2:
                            st.metric("SEO", f"{content.get('seo_score', 85)}/100")
                        with col3:
                            st.metric("가독성", content.get('readability', '높음'))
                        
                        st.markdown("---")
                        
                        # 편집기 툴바
                        st.markdown('<div class="editor-toolbar">📝 편집기</div>', unsafe_allow_html=True)
                        
                        # 제목 (있는 경우)
                        if 'title' in content:
                            edited_title = st.text_input(
                                "제목",
                                value=content['title'],
                                key=f"title_{channel_name}_{ver_idx}"
                            )
                            content['title'] = edited_title
                        
                        if 'subject' in content:
                            edited_subject = st.text_input(
                                "이메일 제목",
                                value=content['subject'],
                                key=f"subject_{channel_name}_{ver_idx}"
                            )
                            content['subject'] = edited_subject
                        
                        # 본문
                        if 'content' in content:
                            edited_content = st.text_area(
                                "본문",
                                value=content['content'],
                                height=400,
                                key=f"content_{channel_name}_{ver_idx}"
                            )
                            content['content'] = edited_content
                        
                        # 트위터 포스트
                        if 'posts' in content:
                            for post_idx, post in enumerate(content['posts']):
                                edited_post = st.text_area(
                                    f"트윗 {post_idx + 1}",
                                    value=post,
                                    height=100,
                                    key=f"post_{channel_name}_{ver_idx}_{post_idx}"
                                )
                                content['posts'][post_idx] = edited_post
                        
                        # 액션 버튼
                        st.markdown("---")
                        col_a1, col_a2, col_a3 = st.columns(3)
                        
                        with col_a1:
                            if st.button("📋 복사", key=f"copy_{channel_name}_{ver_idx}", use_container_width=True):
                                st.success("✅ 복사됨!")
                        
                        with col_a2:
                            content_text = content.get('content', '') or '\n'.join(content.get('posts', []))
                            st.download_button(
                                "💾 다운로드",
                                data=content_text,
                                file_name=f"{channel_name}_v{ver_idx+1}.txt",
                                key=f"download_{channel_name}_{ver_idx}",
                                use_container_width=True
                            )
                        
                        with col_a3:
                            if st.button("🔄 재생성", key=f"regen_{channel_name}_{ver_idx}", use_container_width=True):
                                st.info("재생성 기능은 곧 추가됩니다")
        
        # 전체 초기화 버튼
        st.markdown("---")
        if st.button("🔄 새로 시작", use_container_width=True):
            st.session_state.generated_contents = {}
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9ca3af; padding: 2rem;">
    <p>Made with ❤️ for AI Hackathon | Powered by Groq AI</p>
</div>
""", unsafe_allow_html=True)
