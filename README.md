# mini-pc-playground

GMKtec K8 Plus (Ryzen 7 8845HS / 32GB / 500GB) 기반 AI 놀이터

## 구조

```
mini-pc-playground/
├── docker/          # 컨테이너 환경 (로컬 → AWS 이식 가능)
└── agents/
    ├── schedule/    # 일정 관리 에이전트 (Google Calendar + OneNote)
    └── budget/      # 가계부 에이전트
```

## 환경

- **로컬**: GMKtec K8 Plus, Windows 11 Pro, WSL2 + Docker Desktop
- **클라우드**: AWS EC2 (동일한 docker-compose.yml 사용)
- **고정 IP**: 192.168.200.103

## 설치된 도구

| 도구 | 버전 | 상태 |
|------|------|------|
| Git | 2.54.0 | ✅ |
| GitHub CLI | 2.92.0 | ✅ (로그인 필요) |
| Docker Desktop | 4.71.0 | ✅ (첫 실행 필요) |
| Tailscale | 1.92.5 | ✅ (로그인 필요) |
| Chocolatey | 2.7.1 | ✅ |
| WSL2 + Ubuntu | - | ✅ |

## 남은 수동 작업

1. **Tailscale 로그인**: 미니PC에서 `tailscale login` 실행
2. **Docker Desktop 첫 실행**: 바탕화면에서 실행 후 WSL2 연동 확인
3. **GitHub CLI 로그인**: 미니PC에서 `gh auth login` 실행
4. **Wake on LAN 설정**: 바이오스 + 윈도우 네트워크 어댑터
5. **공유기 포트포워딩 제거**: 딜라이브 고객센터 1644-1188
