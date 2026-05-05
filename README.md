# mini-pc-playground

GMKtec K8 Plus 미니PC AI 에이전트 서버

## 시스템 구조

```
[Desktop / Phone]
       ↓ SSH (터미널)
   [Mini PC]
   ├── tmux → claude (개발/대화용)
   └── Docker Compose
       ├── weather-agent (Claude Haiku + KakaoTalk)
       ├── (예정) schedule-agent
       ├── (예정) budget-agent
       ├── MCP Server (OneDrive/Notion/GitHub)
       └── KakaoTalk (나에게 보내기 + 의 수신)
            ↓
       [Claude API]
```

## 핵심 원칙

- **Docker 필수**: 컨테이너로 어디든 이전 가능
- **터미널 퍼스트**: SSH → miniPC → tmux → claude
- **Claude API**: 에이전트 자동화 (Haiku: 단순작업, Sonnet: 복잡한 분석)
- **KakaoTalk**: 에이전트 채널 (나에게 보내기 + 카카오 톡 채널 명령)

## 날씨 에이전트 (agents/weather)

### 기능
- 매일 07:00 강남구 날씨 → Claude Haiku 요약 → 카카오톡 나에게 발송
- 카카오 톡 채널에서 `날씨` 명령 수신 → 즉시 조회 발송
- 카카오 톡 채널에서 자유 질문 → Claude Haiku 답변

### 시작 순서

**1. 환경 변수 설정**
```bash
cp .env.example .env
# .env 파일에 키 입력
```

**2. 카카오 최초 인증** (1회만)
```bash
# miniPC에서
# developers.kakao.com > 앱 등록 > Redirect URI: http://localhost:5000/kakao/callback
pip install requests python-dotenv
python scripts/kakao_auth.py
# 브라우저에서 URL 열고 로그인 → code 값 입력
# data/kakao_token.json 생성 확인
```

**3. 카카오 챗봇 채널 Webhook** (miniPC 외부 노칠 필요)
```bash
# Cloudflare Tunnel 또는 ngrok·ddns 등으로
# https://your-public-url/kakao/webhook 
# 카카오디벨로퍼스 > 체널 뮨신저 > Webhook URL 에 등록
```

**4. Docker 실행**
```bash
docker compose up -d
docker compose logs -f weather-agent
```

## SSH 접속

```bash
ssh -i ~/.ssh/id_ed25519 dlawo@192.168.200.103
# Tailscale: ssh dlawo@100.113.229.59
```

## 저장소

- Notion: 에이전트 output/정리
- OneDrive: 대용량 파일
- GitHub: 코드 (JHlim-ui/mini-pc-playground)
