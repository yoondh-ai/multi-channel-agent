"""콘텐츠 템플릿 및 설정"""

CONTENT_TEMPLATES = {
    "blog_post": {
        "name": "블로그 포스트",
        "description": "SEO 최적화된 긴 형식의 블로그 아티클",
        "features": [
            "SEO 키워드 최적화",
            "구조화된 섹션",
            "읽기 쉬운 형식",
            "CTA 포함"
        ],
        "recommended_length": "1,500-2,500자"
    },
    "twitter_thread": {
        "name": "트위터 스레드",
        "description": "임팩트 있는 트윗 시리즈",
        "features": [
            "각 트윗 280자 이내",
            "해시태그 포함",
            "이모지 활용",
            "스레드 형식"
        ],
        "recommended_length": "3-7개 트윗"
    },
    "linkedin_post": {
        "name": "LinkedIn 포스트",
        "description": "B2B 전문가 네트워크용 콘텐츠",
        "features": [
            "전문적인 톤",
            "인사이트 중심",
            "네트워킹 유도",
            "비즈니스 가치 강조"
        ],
        "recommended_length": "800-1,200자"
    },
    "instagram_caption": {
        "name": "Instagram 캡션",
        "description": "시각적 콘텐츠를 위한 매력적인 캡션",
        "features": [
            "짧고 임팩트 있는 메시지",
            "이모지 활용",
            "해시태그 전략",
            "스토리텔링"
        ],
        "recommended_length": "150-300자"
    },
    "card_news": {
        "name": "카드뉴스",
        "description": "슬라이드 형식의 비주얼 콘텐츠",
        "features": [
            "5-10장 구성",
            "각 슬라이드별 핵심 메시지",
            "시각적 요소 고려",
            "스토리 플로우"
        ],
        "recommended_length": "5-10개 슬라이드"
    },
    "marketing_email": {
        "name": "마케팅 이메일",
        "description": "뉴스레터 및 프로모션 이메일",
        "features": [
            "매력적인 제목",
            "명확한 CTA",
            "개인화 요소",
            "모바일 최적화"
        ],
        "recommended_length": "500-800자"
    },
    "product_launch": {
        "name": "제품 출시 이메일",
        "description": "신제품 런칭 공지",
        "features": [
            "제품 가치 강조",
            "얼리버드 혜택",
            "긴급성 조성",
            "명확한 액션"
        ],
        "recommended_length": "600-1,000자"
    },
    "press_release": {
        "name": "보도자료",
        "description": "공식 발표용 보도자료",
        "features": [
            "공식적인 톤",
            "5W1H 구조",
            "인용구 포함",
            "연락처 정보"
        ],
        "recommended_length": "800-1,200자"
    },
    "case_study": {
        "name": "케이스 스터디",
        "description": "고객 성공 사례",
        "features": [
            "문제-해결-결과 구조",
            "구체적인 수치",
            "고객 인용",
            "신뢰성 강조"
        ],
        "recommended_length": "1,200-2,000자"
    },
    "whitepaper": {
        "name": "백서",
        "description": "전문적인 기술 문서",
        "features": [
            "심층 분석",
            "데이터 기반",
            "전문가 관점",
            "다운로드 가능"
        ],
        "recommended_length": "2,000-5,000자"
    },
    "google_ads": {
        "name": "Google 광고",
        "description": "검색 광고 카피",
        "features": [
            "제목 30자 이내",
            "설명 90자 이내",
            "키워드 포함",
            "명확한 혜택"
        ],
        "recommended_length": "제목+설명 2-3세트"
    },
    "social_ads": {
        "name": "소셜 미디어 광고",
        "description": "Facebook, Instagram 광고",
        "features": [
            "시선 끄는 헤드라인",
            "감성적 메시지",
            "명확한 CTA",
            "타겟 맞춤"
        ],
        "recommended_length": "100-150자"
    }
}

TONE_OPTIONS = {
    "전문적": "신뢰감 있고 권위 있는 톤. B2B 고객에게 적합",
    "친근한": "편안하고 접근하기 쉬운 톤. 일반 소비자에게 적합",
    "유머러스": "재치 있고 즐거운 톤. 젊은 타겟층에게 적합",
    "긴급한": "행동을 유도하는 강력한 톤. 프로모션에 적합",
    "교육적": "정보 전달 중심의 톤. 가이드나 튜토리얼에 적합",
    "감성적": "공감과 스토리텔링 중심. 브랜드 스토리에 적합",
    "혁신적": "미래지향적이고 트렌디한 톤. 기술 제품에 적합"
}

AUDIENCE_OPTIONS = {
    "C-레벨 임원": "CEO, CTO, CISO 등 의사결정권자",
    "IT 담당자": "시스템 관리자, 보안 담당자",
    "마케팅 담당자": "마케팅 매니저, CMO",
    "중소기업 대표": "스타트업 및 중소기업 경영자",
    "일반 소비자": "B2C 고객",
    "개발자": "소프트웨어 엔지니어, 개발자",
    "학생/교육자": "학생, 교수, 연구원"
}

LENGTH_MAPPING = {
    "짧게": {
        "blog": 800,
        "email": 300,
        "social": 100
    },
    "보통": {
        "blog": 1500,
        "email": 600,
        "social": 200
    },
    "길게": {
        "blog": 2500,
        "email": 1000,
        "social": 300
    }
}
