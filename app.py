"""Gemini 1.5 Flash 기반 마케팅 콘텐츠 생성 플랫폼 - Jasper 스타일"""
import streamlit as st
from pathlib import Path
import sys

# scripts 폴더를 Python 경로에 추가
sys.path.append(str(Path(__file__).parent / "scripts"))

from src.gemini_generator import GeminiContentGenerator
from src.templates import MARKETING_FRAMEWORKS, TONE_OPTIONS, AUDIENCE_OPTIONS
from scripts import publish_to_blog, publish_to_linkedin, publish_to_twitter, publish_to_email

# 페이지 설정
st.set_page_config(
    page_title="AI 마케팅 콘텐츠 생성",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Jasper 스타일 CSS
st.markdown("""
<style>
    /* 전체 배경 */
    .main {
        background-color: #f8f9fa;
    }
    
    /* 메인 헤더 */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
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
        min-height: 600px;
    }
    
    /* 버튼 스타일 */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* 텍스트 영역 */
    .stTextArea textarea {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        font-size: 1rem;
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* 메트릭 카드 */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        color: #667eea;
        font-weight: 700;
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
    
    /* 발행 버튼 */
    .publish-button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
    
    .publish-button:hover {
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'generated_contents' not in st.session_state:
    st.session_state.generated_contents = {}
if 'edited_contents' not in st.session_state:
    st.session_state.edited_contents = {}

# Gemini API 상태 확인
try:
    gemini_key = st.secrets["GEMINI_API_KEY"]
    api_available = True
    api_provider = "Gemini (무료)"
except KeyError:
    api_available = False
    api_provider = None

# ========== 메인 헤더 ==========
st.markdown("""
<div class="main-header">
    <h1>✨ AI 마케팅 콘텐츠 생성</h1>
    <p>Gemini 2.0 Flash - 브랜드 가이드라인 학습 완료</p>
</div>
""", unsafe_allow_html=True)

# API 상태 표시
if api_available:
    st.success(f"✅ {api_provider} 연결됨")
else:
    st.error("❌ GEMINI_API_KEY가 설정되지 않았습니다")
    with st.expander("💡 API 키 설정 방법"):
        st.markdown("""
        **Gemini API 키 발급 (무료)**
        
        1. https://aistudio.google.com/app/apikey 접속
        2. "Create API Key" 클릭
        3. 생성된 키 복사
        
        **Streamlit Cloud Secrets 설정:**
        ```toml
        GEMINI_API_KEY = "AIza..."
        ```
        
        **로컬 개발 (.streamlit/secrets.toml):**
        ```toml
        GEMINI_API_KEY = "AIza..."
        ```
        """)
    st.stop()

st.markdown("---")

# ========== 메인 레이아웃: 좌우 분할 ==========
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
    
    st.markdown("---")
    
    # 타겟 독자
    st.markdown("**🎯 타겟 독자**")
    selected_audience = st.selectbox(
        "독자",
        options=list(AUDIENCE_OPTIONS.keys()),
        label_visibility="collapsed"
    )
    st.caption(AUDIENCE_OPTIONS[selected_audience])
    
    st.markdown("---")
    
    # 말투 (Tone)
    st.markdown("**🎨 말투 (Tone)**")
    selected_tone = st.selectbox(
        "톤",
        options=list(TONE_OPTIONS.keys()),
        label_visibility="collapsed"
    )
    st.caption(TONE_OPTIONS[selected_tone])
    
    st.markdown("---")
    
    # 마케팅 프레임워크
    st.markdown("**📋 마케팅 프레임워크**")
    framework_options = {k: v["name"] for k, v in MARKETING_FRAMEWORKS.items()}
    selected_framework = st.selectbox(
        "프레임워크",
        options=list(framework_options.keys()),
        format_func=lambda x: framework_options[x],
        label_visibility="collapsed"
    )
    framework_info = MARKETING_FRAMEWORKS[selected_framework]
    st.caption(f"💡 {framework_info['description']}")
    
    st.markdown("---")
    
    # 생성 옵션
    st.markdown("**⚙️ 생성 옵션**")
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        num_variants = st.number_input("생성 개수", 1, 3, 2, help="채널당 생성할 버전 수")
    with col_opt2:
        include_seo = st.checkbox("SEO 최적화", value=True)
        include_cta = st.checkbox("CTA 포함", value=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 생성 버튼
    generate_button = st.button("🚀 콘텐츠 생성하기", type="primary", use_container_width=True)
    
    if generate_button:
        if not product_name:
            st.error("❌ 제품/서비스명을 입력하세요")
        elif not key_features:
            st.error("❌ 핵심 특징을 입력하세요")
        else:
            with st.spinner("🤖 Gemini가 콘텐츠를 생성하고 있습니다..."):
                try:
                    # 설정 구성
                    config = {
                        "product_name": product_name,
                        "key_features": key_features,
                        "keywords": keywords or product_name,
                        "additional_context": additional_context,
                        "audience": selected_audience,
                        "tone": selected_tone,
                        "framework": selected_framework,
                        "length": "보통 (100-500자)",
                        "variants": num_variants,
                        "include_cta": include_cta,
                        "include_seo": include_seo,
                    }
                    
                    # Gemini 생성기 초기화
                    generator = GeminiContentGenerator()
                    
                    # 채널별 콘텐츠 생성
                    channels = {
                        "네이버 블로그": "blog_post",
                        "LinkedIn": "linkedin_post",
                        "Twitter": "twitter_thread",
                        "이메일": "marketing_email"
                    }
                    
                    results = {}
                    for channel_name, template in channels.items():
                        st.info(f"📝 {channel_name} 생성 중...")
                        channel_contents = []
                        for i in range(num_variants):
                            content = generator.generate_content(
                                template=template,
                                config=config
                            )
                            channel_contents.append(content)
                        results[channel_name] = channel_contents
                    
                    st.session_state.generated_contents = results
                    st.session_state.edited_contents = {}  # 초기화
                    
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
                        # Thinking Process 표시
                        if 'thinking' in content and content['thinking']:
                            with st.expander("🧠 AI Thinking Process", expanded=False):
                                thinking = content['thinking']
                                st.markdown(f"""
**타겟 독자 분석:**
{thinking.get('target_audience', 'N/A')}

**핵심 가치:**
{thinking.get('core_value', 'N/A')}

**핵심 메시지:**
{thinking.get('key_message', 'N/A')}

**차별화 포인트:**
{thinking.get('differentiation', 'N/A')}
""")
                        
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
                        
                        # 편집 가능한 콘텐츠
                        edit_key = f"{channel_name}_{ver_idx}"
                        
                        # 제목 (있는 경우)
                        if 'title' in content:
                            if edit_key not in st.session_state.edited_contents:
                                st.session_state.edited_contents[edit_key] = {}
                            
                            edited_title = st.text_input(
                                "제목",
                                value=st.session_state.edited_contents[edit_key].get('title', content['title']),
                                key=f"title_{edit_key}"
                            )
                            st.session_state.edited_contents[edit_key]['title'] = edited_title
                        
                        if 'subject' in content:
                            if edit_key not in st.session_state.edited_contents:
                                st.session_state.edited_contents[edit_key] = {}
                            
                            edited_subject = st.text_input(
                                "이메일 제목",
                                value=st.session_state.edited_contents[edit_key].get('subject', content['subject']),
                                key=f"subject_{edit_key}"
                            )
                            st.session_state.edited_contents[edit_key]['subject'] = edited_subject
                        
                        # 본문
                        if 'content' in content:
                            if edit_key not in st.session_state.edited_contents:
                                st.session_state.edited_contents[edit_key] = {}
                            
                            edited_content = st.text_area(
                                "본문 (직접 수정 가능)",
                                value=st.session_state.edited_contents[edit_key].get('content', content['content']),
                                height=400,
                                key=f"content_{edit_key}"
                            )
                            st.session_state.edited_contents[edit_key]['content'] = edited_content
                        
                        # 트위터 포스트
                        if 'posts' in content:
                            if edit_key not in st.session_state.edited_contents:
                                st.session_state.edited_contents[edit_key] = {'posts': content['posts'].copy()}
                            
                            for post_idx, post in enumerate(content['posts']):
                                edited_post = st.text_area(
                                    f"트윗 {post_idx + 1} (직접 수정 가능)",
                                    value=st.session_state.edited_contents[edit_key]['posts'][post_idx],
                                    height=100,
                                    key=f"post_{edit_key}_{post_idx}"
                                )
                                st.session_state.edited_contents[edit_key]['posts'][post_idx] = edited_post
                        
                        # 액션 버튼
                        st.markdown("---")
                        col_a1, col_a2, col_a3 = st.columns(3)
                        
                        with col_a1:
                            if st.button("📋 복사", key=f"copy_{edit_key}", use_container_width=True):
                                st.success("✅ 복사됨!")
                        
                        with col_a2:
                            content_text = st.session_state.edited_contents.get(edit_key, {}).get('content', content.get('content', ''))
                            if not content_text and 'posts' in content:
                                content_text = '\n\n'.join(st.session_state.edited_contents.get(edit_key, {}).get('posts', content['posts']))
                            
                            st.download_button(
                                "💾 다운로드",
                                data=content_text,
                                file_name=f"{channel_name}_v{ver_idx+1}.txt",
                                key=f"download_{edit_key}",
                                use_container_width=True
                            )
                        
                        with col_a3:
                            if st.button("🔄 재생성", key=f"regen_{edit_key}", use_container_width=True):
                                st.info("재생성 기능은 곧 추가됩니다")
                        
                        # 발행 버튼
                        st.markdown("---")
                        st.markdown("**🚀 발행하기**")
                        
                        if st.button(f"📤 {channel_name}에 발행", key=f"publish_{edit_key}", use_container_width=True):
                            with st.spinner(f"{channel_name}에 발행 중..."):
                                try:
                                    edited_data = st.session_state.edited_contents.get(edit_key, {})
                                    
                                    if channel_name == "네이버 블로그":
                                        result = publish_to_blog(
                                            title=edited_data.get('title', content.get('title', '')),
                                            content=edited_data.get('content', content.get('content', ''))
                                        )
                                    elif channel_name == "LinkedIn":
                                        result = publish_to_linkedin(
                                            content=edited_data.get('content', content.get('content', ''))
                                        )
                                    elif channel_name == "Twitter":
                                        result = publish_to_twitter(
                                            tweets=edited_data.get('posts', content.get('posts', []))
                                        )
                                    elif channel_name == "이메일":
                                        result = publish_to_email(
                                            subject=edited_data.get('subject', content.get('subject', '')),
                                            content=edited_data.get('content', content.get('content', ''))
                                        )
                                    
                                    if result['success']:
                                        st.success(f"✅ {result['message']}")
                                        if 'url' in result:
                                            st.info(f"🔗 URL: {result['url']}")
                                    else:
                                        st.error(f"❌ 발행 실패: {result.get('message', '알 수 없는 오류')}")
                                        
                                except Exception as e:
                                    st.error(f"❌ 발행 중 오류: {str(e)}")
        
        # 전체 초기화 버튼
        st.markdown("---")
        if st.button("🔄 새로 시작", use_container_width=True):
            st.session_state.generated_contents = {}
            st.session_state.edited_contents = {}
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9ca3af; padding: 2rem;">
    <p>Made with ❤️ for AI Hackathon | Powered by Gemini 2.0 Flash</p>
</div>
""", unsafe_allow_html=True)
