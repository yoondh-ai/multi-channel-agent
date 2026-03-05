"""Jasper AI 스타일 마케팅 콘텐츠 생성 플랫폼 - 개선된 레이아웃"""
import streamlit as st
from dotenv import load_dotenv
import os
from datetime import datetime
from src.agent_v2 import MarketingContentAgent
from src.templates import CONTENT_TEMPLATES, TONE_OPTIONS, AUDIENCE_OPTIONS, LENGTH_MAPPING

# 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="AI 마케팅 콘텐츠 생성 플랫폼",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS
st.markdown("""
<style>
    /* 모든 상단 여백 강제 제거 */
    .main .block-container {
        padding-top: 0rem !important;
        padding-left: 1rem;
        padding-right: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* 헤더 */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-top: 0 !important;
        margin-bottom: 0rem !important;
    }
    
    /* 왼쪽 패널 스타일 제거 - 직접 적용 안 함 */
    
    /* 오른쪽 콘텐츠 영역 스타일 제거 - 직접 적용 안 함 */
    
    /* 섹션 구분선 */
    .section-divider {
        border-top: 2px solid #e0e0e0;
        margin: 1.5rem 0;
    }
    
    /* 버튼 */
    .stButton button {
        border-radius: 8px;
    }
    
    /* Streamlit 기본 여백 완전 제거 */
    .element-container {
        margin-bottom: 0.5rem !important;
        margin-top: 0 !important;
    }
    
    /* 상단 헤더 영역 제거 */
    header[data-testid="stHeader"] {
        display: none;
    }
    
    /* 메인 영역 상단 패딩 제거 */
    .main {
        padding-top: 0 !important;
    }
    
    /* 첫 번째 div 여백 제거 */
    .main > div:first-child {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* 모든 상단 여백 제거 */
    div[data-testid="stVerticalBlock"] > div:first-child {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* 컬럼 간격 제거 */
    div[data-testid="column"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* 수평 블록 여백 제거 */
    div[data-testid="stHorizontalBlock"] {
        gap: 1rem !important;
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* 모든 div 상단 여백 제거 */
    .stMarkdown {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'generated_contents' not in st.session_state:
    st.session_state.generated_contents = []
if 'history' not in st.session_state:
    st.session_state.history = []
if 'selected_template' not in st.session_state:
    st.session_state.selected_template = None
if 'brand_name' not in st.session_state:
    st.session_state.brand_name = "MarkAny"
if 'brand_values' not in st.session_state:
    st.session_state.brand_values = "혁신, 신뢰, 보안"

# 헤더
st.markdown("""
<div class="main-header">
    <h1>✨ AI 마케팅 콘텐츠 생성 플랫폼</h1>
    <p>보안 기술을 고객의 마음을 사로잡는 마케팅 콘텐츠로 변환</p>
</div>
""", unsafe_allow_html=True)

# API 상태
openai_key = os.getenv("OPENAI_API_KEY")
gemini_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

# API 키 유효성 간단 체크
api_key_valid = False
api_provider = None

if gemini_key:
    api_key_valid = True
    api_provider = "Gemini"
    st.success("✅ Gemini AI 연결됨 - 실제 콘텐츠 생성 가능")
elif openai_key:
    if openai_key.startswith("sk-") and len(openai_key) > 20:
        api_key_valid = True
        api_provider = "OpenAI"
        st.success("✅ OpenAI 연결됨 - 실제 콘텐츠 생성 가능")
    else:
        st.error("❌ OpenAI API 키 형식이 올바르지 않습니다")
        openai_key = None
else:
    st.warning("⚠️ 데모 모드 - 샘플 콘텐츠로 작동합니다")

if not api_key_valid:
    with st.expander("💡 API 키 설정 방법"):
        st.markdown("""
        **옵션 1: Google Gemini (추천 - 무료)**
        
        Streamlit Cloud Secrets에 추가:
        ```
        GOOGLE_API_KEY = "your-gemini-api-key"
        ```
        
        API 키 발급:
        1. https://aistudio.google.com/app/apikey 접속
        2. "Create API key" 클릭
        3. Google Workspace 계정으로 로그인
        4. 생성된 키 복사
        
        ---
        
        **옵션 2: OpenAI (유료)**
        
        Streamlit Cloud Secrets에 추가:
        ```
        OPENAI_API_KEY = "sk-proj-실제키입력"
        ```
        
        API 키 발급:
        - https://platform.openai.com/api-keys
        - 결제 정보 등록 필요
        
        ---
        
        **주의:**
        - Gemini는 Google Workspace 계정으로 무료 사용 가능
        - OpenAI는 사용량에 따라 과금됨
        """)

st.markdown("---")

# 메인 레이아웃: 왼쪽 1/4, 오른쪽 3/4
left_col, right_col = st.columns([1, 3], gap="small")

# ========== 왼쪽: 입력 패널 ==========
with left_col:
    # 1. 템플릿 선택
    st.subheader("1️⃣ 템플릿")
    
    template_categories = {
        "📝 블로그": ["blog_post", "case_study", "whitepaper"],
        "📱 SNS": ["twitter_thread", "linkedin_post", "instagram_caption", "card_news"],
        "📧 이메일": ["marketing_email", "product_launch"],
        "🎯 광고": ["google_ads", "social_ads"]
    }
    
    # 카테고리 선택
    category_names = list(template_categories.keys())
    selected_category = st.selectbox(
        "카테고리",
        options=category_names,
        index=0
    )
    
    # 선택된 카테고리의 템플릿 목록
    templates_in_category = template_categories[selected_category]
    template_options = {
        template_key: CONTENT_TEMPLATES[template_key]['name']
        for template_key in templates_in_category
    }
    
    # 현재 선택된 템플릿이 이 카테고리에 있는지 확인
    default_index = 0
    if st.session_state.selected_template in templates_in_category:
        default_index = templates_in_category.index(st.session_state.selected_template)
    
    # 템플릿 선택
    selected_template = st.selectbox(
        "템플릿",
        options=list(template_options.keys()),
        format_func=lambda x: template_options[x],
        index=default_index
    )
    
    st.session_state.selected_template = selected_template
    
    # 선택된 템플릿 정보 표시
    if selected_template:
        template_info = CONTENT_TEMPLATES[selected_template]
        st.info(f"**{template_info['name']}**\n\n{template_info['description']}")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # 2. 기본 정보
    st.subheader("2️⃣ 기본 정보")
    keywords = st.text_input("핵심 키워드", placeholder="예: 제로트러스트")
    description = st.text_area("상세 설명", placeholder="구체적으로 작성", height=100)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # 3. 타겟
    st.subheader("3️⃣ 타겟")
    audience = st.selectbox("대상", list(AUDIENCE_OPTIONS.keys()))
    industry = st.text_input("산업", placeholder="예: IT, 금융")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # 4. 스타일
    st.subheader("4️⃣ 스타일")
    tone = st.selectbox("톤앤매너", list(TONE_OPTIONS.keys()))
    st.caption(TONE_OPTIONS[tone])
    
    length = st.selectbox("길이", list(LENGTH_MAPPING.keys()))
    st.caption(LENGTH_MAPPING[length]['description'])
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # 5. 옵션
    st.subheader("5️⃣ 옵션")
    variants = st.number_input("생성 개수", 1, 5, 3)
    include_cta = st.checkbox("CTA 포함", value=True)
    include_seo = st.checkbox("SEO 최적화", value=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # 6. 브랜드
    with st.expander("🎨 브랜드"):
        brand_name = st.text_input("브랜드명", value=st.session_state.brand_name)
        brand_values = st.text_area("핵심 가치", value=st.session_state.brand_values, height=60)
        st.session_state.brand_name = brand_name
        st.session_state.brand_values = brand_values
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # 7. 레퍼런스 학습
    st.subheader("6️⃣ 레퍼런스 학습")
    
    use_reference = st.checkbox("기존 콘텐츠 스타일 참고", value=False)
    
    reference_source = None
    reference_url = None
    reference_text = None
    
    if use_reference:
        reference_type = st.radio(
            "참고 소스",
            ["우리 회사 콘텐츠", "경쟁사/업계 리더 콘텐츠", "직접 입력"],
            horizontal=True
        )
        
        if reference_type == "우리 회사 콘텐츠":
            st.caption("자사 블로그/SNS의 톤앤매너를 학습합니다")
            reference_url = st.text_input(
                "블로그/SNS URL",
                placeholder="예: https://blog.markany.com/...",
                help="분석할 콘텐츠의 URL을 입력하세요"
            )
            reference_source = "company"
            
        elif reference_type == "경쟁사/업계 리더 콘텐츠":
            st.caption("벤치마킹할 기업의 스타일을 학습합니다")
            
            col_ref1, col_ref2 = st.columns(2)
            with col_ref1:
                competitor_name = st.text_input(
                    "기업명",
                    placeholder="예: Palo Alto Networks"
                )
            with col_ref2:
                reference_url = st.text_input(
                    "콘텐츠 URL",
                    placeholder="블로그/SNS 링크"
                )
            reference_source = f"competitor:{competitor_name}"
            
        else:  # 직접 입력
            st.caption("참고할 콘텐츠를 직접 붙여넣으세요")
            reference_text = st.text_area(
                "레퍼런스 텍스트",
                placeholder="참고할 콘텐츠를 붙여넣으세요 (최대 1000자)",
                height=150,
                max_chars=1000
            )
            reference_source = "manual"
        
        if reference_url or reference_text:
            st.info("💡 AI가 이 콘텐츠의 톤, 문체, 구조를 분석하여 유사한 스타일로 생성합니다")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # 생성 버튼
    if st.button("✨ 콘텐츠 생성", type="primary", use_container_width=True):
        if not selected_template:
            st.error("템플릿을 선택하세요")
        elif not keywords:
            st.error("키워드를 입력하세요")
        else:
            with st.spinner("🤖 생성 중..."):
                try:
                    config = {
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
                        "brand_values": brand_values,
                        "use_reference": use_reference,
                        "reference_source": reference_source,
                        "reference_url": reference_url,
                        "reference_text": reference_text
                    }
                    
                    agent = MarketingContentAgent()
                    contents = agent.generate_content(
                        template=selected_template,
                        config=config,
                        use_mock=(not openai_key and not gemini_key)
                    )
                    
                    st.session_state.generated_contents = contents
                    
                    st.session_state.history.append({
                        "template": CONTENT_TEMPLATES[selected_template]['name'],
                        "keywords": keywords,
                        "contents": contents,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    if not openai_key and not gemini_key:
                        st.warning("⚠️ 데모 모드: API 키가 없어 샘플 콘텐츠를 생성했습니다.")
                    
                    st.success(f"✅ {len(contents)}개 완료! ({api_provider or '데모'} 사용)")
                    st.rerun()
                    
                except Exception as e:
                    error_msg = str(e)
                    
                    # API 키 오류 처리
                    if "429" in error_msg or "insufficient_quota" in error_msg:
                        st.error("❌ OpenAI API 할당량이 초과되었습니다.")
                        st.info("""
                        **해결 방법:**
                        
                        **옵션 1: Gemini로 전환 (추천)**
                        1. https://aistudio.google.com/app/apikey 에서 API 키 발급
                        2. Streamlit Cloud Settings → Secrets에 추가:
                           ```
                           GOOGLE_API_KEY = "your-gemini-key"
                           ```
                        3. 앱 재시작
                        
                        **옵션 2: OpenAI 결제**
                        - https://platform.openai.com/account/billing
                        - 결제 정보 등록 및 크레딧 충전
                        """)
                    elif "401" in error_msg or "invalid_api_key" in error_msg:
                        st.error("❌ API 키가 유효하지 않습니다.")
                        st.info("Secrets에서 API 키를 확인하거나 Gemini로 전환하세요.")
                    else:
                        st.error(f"오류: {error_msg}")
                        st.exception(e)
    
    if st.session_state.generated_contents:
        if st.button("🔄 새로 시작", use_container_width=True):
            st.session_state.generated_contents = []
            st.session_state.selected_template = None
            st.rerun()

# ========== 오른쪽: 결과 패널 ==========
with right_col:
    
    if not st.session_state.generated_contents:
        st.markdown("""
        <div style="text-align: center; padding: 8rem 2rem; color: #999;">
            <h2>👈 왼쪽에서 설정 후 콘텐츠를 생성하세요</h2>
            <p style="margin-top: 1rem;">AI가 여러 버전을 자동 생성합니다</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.header("📊 생성된 콘텐츠")
        
        tabs = st.tabs([f"✨ 버전 {i+1}" for i in range(len(st.session_state.generated_contents))])
        
        for i, (tab, content) in enumerate(zip(tabs, st.session_state.generated_contents)):
            with tab:
                # 메트릭
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                
                with col_m1:
                    if 'content' in content:
                        char_count = len(content['content'])
                        st.metric("글자 수", f"{char_count}자")
                    elif 'posts' in content:
                        st.metric("포스트", f"{len(content['posts'])}개")
                
                with col_m2:
                    st.metric("SEO", f"{content.get('seo_score', 85)}/100")
                
                with col_m3:
                    st.metric("가독성", content.get('readability', '높음'))
                
                with col_m4:
                    st.metric("버전", f"#{i+1}")
                
                st.markdown("---")
                
                # 콘텐츠 편집
                if 'title' in content:
                    st.subheader("📝 제목")
                    edited_title = st.text_input(
                        "제목",
                        value=content['title'],
                        key=f"title_{i}",
                        label_visibility="collapsed"
                    )
                    content['title'] = edited_title
                
                if 'subject' in content:
                    st.subheader("📧 제목")
                    edited_subject = st.text_input(
                        "제목",
                        value=content['subject'],
                        key=f"subject_{i}",
                        label_visibility="collapsed"
                    )
                    content['subject'] = edited_subject
                
                if 'content' in content:
                    st.subheader("📄 본문")
                    edited_content = st.text_area(
                        "본문",
                        value=content['content'],
                        height=400,
                        key=f"content_{i}",
                        label_visibility="collapsed"
                    )
                    content['content'] = edited_content
                
                if 'posts' in content:
                    st.subheader("📱 포스트")
                    for j, post in enumerate(content['posts']):
                        edited_post = st.text_area(
                            f"포스트 {j+1}",
                            value=post,
                            height=120,
                            key=f"post_{i}_{j}"
                        )
                        content['posts'][j] = edited_post
                
                if 'ads' in content:
                    st.subheader("🎯 광고")
                    for j, ad in enumerate(content['ads']):
                        with st.expander(f"세트 {j+1}", expanded=True):
                            for key, value in ad.items():
                                st.text_input(key, value, key=f"ad_{i}_{j}_{key}")
                
                # 액션
                st.markdown("---")
                col_a1, col_a2, col_a3 = st.columns(3)
                
                with col_a1:
                    if st.button("📋 복사", key=f"copy_{i}", use_container_width=True):
                        st.success("복사됨!")
                
                with col_a2:
                    if st.button("⭐ 즐겨찾기", key=f"fav_{i}", use_container_width=True):
                        if 'favorites' not in st.session_state:
                            st.session_state.favorites = []
                        st.session_state.favorites.append(content)
                        st.success("추가됨!")
                
                with col_a3:
                    content_text = content.get('content', '') or '\n'.join(content.get('posts', []))
                    st.download_button(
                        "💾 다운로드",
                        data=content_text,
                        file_name=f"content_v{i+1}.txt",
                        key=f"download_{i}",
                        use_container_width=True
                    )
        
        # 포스팅
        st.markdown("---")
        st.subheader("🚀 포스팅")
        
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            post_blog = st.checkbox("📝 블로그", value=True)
        with col_p2:
            post_twitter = st.checkbox("🐦 트위터", value=True)
        with col_p3:
            post_linkedin = st.checkbox("💼 LinkedIn", value=False)
        
        if st.button("📤 포스팅 실행", type="primary", use_container_width=True):
            with st.spinner("포스팅 중..."):
                import time
                time.sleep(1)
                
                if post_blog:
                    st.success("✅ 블로그 완료 (미리보기)")
                if post_twitter:
                    st.success("✅ 트위터 완료 (미리보기)")
                if post_linkedin:
                    st.success("✅ LinkedIn 완료 (미리보기)")

