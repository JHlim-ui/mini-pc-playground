# mini-pc-playground

GMKtec K8 Plus (Ryzen 7 8845HS / 32GB / 500GB) 기반 AI 놀이터

## 구조

```
mini-pc-playground/
├── docker/          # 컨테이너 환경 (로컬 → AWS 이식 가능)
└── agents/
    ├── schedule/    # 일정 관리 에이전트
    └── budget/      # 가계부 에이전트
```

## 환경

- **로컬**: GMKtec K8 Plus, Windows 11 Pro, WSL2 + Docker Desktop
- **클라우드**: AWS EC2 (동일한 docker-compose.yml 사용)
