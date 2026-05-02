# Mini PC 가지고 놀기

GMKtec K8 Plus 미니PC를 홈 서버로 세팅하고 Claude Agent 자동화를 실험하는 프로젝트.

## 하드웨어 스펙
- CPU: AMD Ryzen 7 8845HS
- RAM: 32GB
- SSD: 500GB
- OS: Windows 11 Pro

## 연결된 외부 서비스
- **GitHub MCP**: 연결 완료 (글로벌 user scope)
- **Notion MCP**: 연결 완료 (글로벌 user scope)
- **Notion 페이지**: "상자의 AI 놀이터" > "Mini PC 가지고 놀기"

## 완료된 작업
- [x] GitHub MCP 연결
- [x] Notion MCP 연결
- [x] GitHub 레포 생성 (JHlim-ui/mini-pc-playground)
- [x] Notion 페이지 생성 (Mini PC 가지고 놀기 + GMKtec K8 Plus 세팅 하위 페이지)

## 다음 할 일
- [ ] Docker Desktop 설치 및 설정
- [ ] WSL2 활성화
- [ ] 고정 IP 설정
- [ ] SSH 원격 접속 설정
- [ ] 첫 Claude Agent 자동화 구현

## 작업 규칙
- 한글이 포함된 API 요청(Notion 등)은 반드시 JSON 파일로 저장 후 `--data-binary @파일경로` 방식으로 전송
- 서브에이전트 호출 최소화 (Pro 세션 한도 절약)
