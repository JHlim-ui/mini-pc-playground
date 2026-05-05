# mini-pc-playground

GMKtec K8 Plus (Ryzen 7 8845HS / 32GB / 500GB) 기반 AI 에이전트 서버

## 시스템 컨셉

여러 AI 에이전트가 자율적으로 동작하며 일상을 보조하는 시스템.
Docker로 감싸서 AWS 또는 다른 Mini PC로 언제든 이전 가능.

```
[Desktop / Phone]
       ↓ SSH (터미널)
   [Mini PC]
       ↓
  [Docker Compose]
  ├── Agent: 일정관리 (Google Calendar + Notion)
  ├── Agent: 가계부
  ├── MCP Server (OneDrive / Notion / GitHub)
  └── Telegram Bot (알림 & 소통 인터페이스)
       ↓
  [Claude API]
```

## 핵심 원칙

- **Docker 필수** — 컨테이너로 감싸서 어디든 이전 가능
- **터미널 퍼스트** — 데스크톱이든 스마트폰이든 SSH로 Mini PC에 직접 접속
- **Claude API** — 에이전트 자동화용 (Haiku: 단순작업 / Sonnet: 복잡한 분석)
- **Claude Code** — 개발/디버깅/대화형 작업용으로 병행
- **Telegram** — 에이전트와 사용자 소통 채널

## 저장소 역할

| 저장소 | 용도 |
|---|---|
| **Notion** | 에이전트 output, 정리, 요약 |
| **OneDrive** | 대용량 파일 |
| **GitHub** | 코드 & 프로젝트 |

## 구조

```
mini-pc-playground/
├── docker/                  # Docker Compose 환경 (로컬 → AWS 이식 가능)
├── agents/
│   ├── schedule/            # 일정관리 에이전트
│   └── budget/              # 가계부 에이전트
└── MCP-Microsoft-Office/    # OneDrive/Calendar/Mail MCP 서버
```

## 환경

- **로컬**: GMKtec K8 Plus, Windows 11 Pro, WSL2 + Docker Desktop
- **클라우드**: AWS EC2 (동일한 docker-compose.yml 사용)
- **접속**: Tailscale (100.113.229.59) 또는 SSH (192.168.200.103)

## 설치된 도구

| 도구 | 버전 | 상태 |
|---|---|---|
| Git | 2.54.0 | ✅ |
| GitHub CLI | 2.92.0 | ✅ |
| Docker Desktop | 4.71.0 | ✅ |
| Tailscale | 1.92.5 | ✅ |
| Node.js | 24.15.0 | ✅ |
| Claude Code | 2.1.126 | ✅ |
| Azure CLI | 2.85.0 | ✅ |

## 남은 작업

- [ ] Claude API Key 발급 (console.anthropic.com)
- [ ] Docker Compose 설계 (에이전트 + MCP + Telegram)
- [ ] Telegram Bot 연동
- [ ] 첫 에이전트 자동화 구현
- [ ] Wake on LAN 설정 (LAN 케이블 연결 후, MAC: C8-FF-BF-0E-58-CE)
