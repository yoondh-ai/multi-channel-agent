# AWS Bedrock Claude 3.5 Sonnet 설정 가이드

## 🎯 왜 AWS Bedrock인가?

### 기존 방식의 한계
- **Groq/OpenAI**: 단순 텍스트 생성
- **키워드만 교체**: 원문 구조 그대로 유지
- **외부 지식 의존**: 주어진 데이터 무시
- **브랜드 톤 불일치**: 가이드라인 미반영

### Bedrock Claude 3.5 Sonnet의 장점
- ✅ **System Prompt 주입**: 브랜드 가이드라인 완벽 학습
- ✅ **Thinking Process**: AI가 글쓰기 전 사고 과정 거침
- ✅ **Data Grounding**: 주어진 데이터에만 기반
- ✅ **Full Paraphrasing**: 문장 구조 완전히 재작성
- ✅ **엔터프라이즈급**: 안정성, 보안, 확장성

## 🚀 설정 방법

### 1단계: AWS 계정 생성
1. https://aws.amazon.com 접속
2. "Create an AWS Account" 클릭
3. 이메일, 비밀번호 입력
4. 결제 정보 등록 (필수)

### 2단계: IAM 사용자 생성

#### AWS Console 접속
1. AWS Management Console 로그인
2. 검색창에 "IAM" 입력
3. IAM 대시보드 접속

#### 사용자 생성
1. 왼쪽 메뉴 "Users" 클릭
2. "Create user" 버튼 클릭
3. User name: `bedrock-user` 입력
4. "Next" 클릭

#### 권한 설정
1. "Attach policies directly" 선택
2. 검색창에 "bedrock" 입력
3. 다음 정책 선택:
   - `AmazonBedrockFullAccess`
4. "Next" 클릭
5. "Create user" 클릭

#### Access Key 생성
1. 생성된 사용자 클릭
2. "Security credentials" 탭
3. "Create access key" 클릭
4. "Application running outside AWS" 선택
5. "Next" 클릭
6. Description: `marketing-agent` 입력
7. "Create access key" 클릭
8. **Access key ID** 복사 (나중에 볼 수 없음!)
9. **Secret access key** 복사 (나중에 볼 수 없음!)

### 3단계: Bedrock 모델 액세스 활성화

#### Bedrock Console 접속
1. AWS Console 검색창에 "Bedrock" 입력
2. Amazon Bedrock 서비스 선택
3. 왼쪽 메뉴 "Model access" 클릭

#### Claude 3.5 Sonnet 활성화
1. "Manage model access" 버튼 클릭
2. "Anthropic" 섹션 찾기
3. "Claude 3.5 Sonnet v2" 체크
4. "Request model access" 클릭
5. 승인 대기 (보통 즉시 승인)

### 4단계: Streamlit Cloud 설정

#### Secrets 추가
1. Streamlit Cloud 앱 대시보드
2. 앱 선택 → Settings (⚙️)
3. Secrets 탭
4. 다음 내용 추가:

```toml
# AWS Bedrock 설정
AWS_ACCESS_KEY_ID = "AKIA..."  # 2단계에서 복사한 Access Key ID
AWS_SECRET_ACCESS_KEY = "..."  # 2단계에서 복사한 Secret Access Key
AWS_REGION = "us-east-1"  # 또는 다른 리전
```

5. "Save" 클릭
6. 앱 자동 재시작 대기 (약 1분)

### 5단계: 로컬 개발 환경 설정 (선택사항)

#### .env 파일 생성
```bash
# multi-channel-agent/.env
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
```

#### 테스트
```bash
cd multi-channel-agent
pip install -r requirements.txt
streamlit run app.py
```

## 📋 브랜드 가이드라인 설정

### 가이드라인 문서 위치
```
multi-channel-agent/
└── .kiro/
    └── steering/
        ├── brand_voice.md          # 브랜드 보이스 가이드
        └── content_guidelines.md   # 콘텐츠 작성 가이드
```

### 커스터마이징

#### 1. 브랜드 보이스 수정
`.kiro/steering/brand_voice.md` 파일 편집:

```markdown
# 우리 회사 브랜드 보이스

## 브랜드 정체성
[회사 소개]

## 핵심 가치
- 가치 1
- 가치 2

## 톤앤매너
[설명]
```

#### 2. 콘텐츠 가이드라인 수정
`.kiro/steering/content_guidelines.md` 파일 편집:

```markdown
# 콘텐츠 작성 원칙

## 작성 원칙
[원칙 설명]

## 금지 표현
[금지 사항]
```

#### 3. 추가 가이드라인
새 파일 생성: `.kiro/steering/seo_guidelines.md`

모든 `.md` 파일이 자동으로 System Prompt에 포함됩니다!

## 🎯 작동 원리

### 1. System Prompt 구성
```
당신은 MarkAny의 전문 마케팅 작성자입니다.

# 브랜드 가이드라인
[brand_voice.md 내용]
[content_guidelines.md 내용]
[기타 .md 파일 내용]

# 작성 원칙
- 데이터 기반 작성
- 완전한 재작성
- Thinking Process
```

### 2. User Prompt 구성
```
# 소스 데이터 (최상단 배치)
제품명: ...
핵심 특징: ...
웹 리서치: ...

# 작성 요구사항
타겟: ...
톤: ...
프레임워크: ...

# 작성 지시
1. Thinking Process 수행
2. 완전히 재작성
3. 데이터에만 기반
```

### 3. Claude 응답
```json
{
  "thinking": {
    "target_audience": "IT 담당자",
    "core_value": "보안 강화",
    "key_message": "제로트러스트로 완벽한 보안",
    "differentiation": "20년 검증된 기술"
  },
  "content": {
    "title": "...",
    "body": "...",
    "cta": "..."
  }
}
```

## 💰 비용

### Bedrock 요금 (Claude 3.5 Sonnet)
- Input: $3.00 / 1M tokens
- Output: $15.00 / 1M tokens

### 예상 비용 (블로그 포스트 1개)
- Input: ~2,000 tokens (가이드라인 + 데이터)
- Output: ~1,000 tokens (콘텐츠)
- 비용: $0.006 + $0.015 = **$0.021 (약 30원)**

### 월 예상 비용
- 하루 10개 콘텐츠 생성
- 월 300개 × $0.021 = **$6.30 (약 9,000원)**

매우 저렴합니다! 🎉

## 🆚 비교

| 항목 | Groq (무료) | Bedrock Claude 3.5 |
|------|-------------|-------------------|
| 비용 | 무료 | ~$0.02/콘텐츠 |
| 브랜드 학습 | ❌ | ✅ System Prompt |
| Thinking Process | ❌ | ✅ 포함 |
| Data Grounding | ⚠️ 부분적 | ✅ 완벽 |
| Paraphrasing | ⚠️ 부분적 | ✅ 완전 재작성 |
| 안정성 | 보통 | 높음 |
| 확장성 | 제한적 | 무제한 |
| 추천 | 테스트용 | 프로덕션 |

## 🔍 확인 방법

### 앱에서 확인
1. Streamlit 앱 새로고침
2. 사이드바 하단 확인:
   ```
   ✅ AWS Bedrock (Claude 3.5 Sonnet) 연결됨
   ```

### 콘솔에서 확인
앱 로그에서:
```
✅ AWS Bedrock 연결됨 (Claude 3.5 Sonnet)
🚀 AWS Bedrock Claude 3.5 Sonnet 사용
🤖 Claude 3.5 Sonnet으로 콘텐츠 생성 중...
```

### 결과에서 확인
생성된 콘텐츠에 "🧠 AI Thinking Process" 섹션 표시

## 🐛 문제 해결

### "Access Denied" 오류
→ IAM 권한 확인
→ `AmazonBedrockFullAccess` 정책 추가

### "Model not found" 오류
→ Bedrock Console에서 모델 액세스 활성화
→ Claude 3.5 Sonnet v2 체크

### "Invalid credentials" 오류
→ Access Key 재확인
→ Secrets에 정확히 입력했는지 확인

### 비용 걱정
→ AWS Budgets 설정
→ 월 $10 알림 설정
→ 실제 비용은 매우 저렴 (~$6/월)

## 📚 추가 리소스

- [AWS Bedrock 문서](https://docs.aws.amazon.com/bedrock/)
- [Claude 3.5 Sonnet 가이드](https://docs.anthropic.com/claude/docs)
- [IAM 사용자 가이드](https://docs.aws.amazon.com/IAM/)

## 🎉 결론

AWS Bedrock Claude 3.5 Sonnet은:
- ✅ 브랜드 가이드라인 완벽 학습
- ✅ Thinking Process로 고품질 콘텐츠
- ✅ Data Grounding으로 정확성 보장
- ✅ Full Paraphrasing으로 독창성 확보
- ✅ 저렴한 비용 (~$6/월)

**프로덕션 환경에 최적입니다!** 🚀

---

*마지막 업데이트: 2024년 3월*
