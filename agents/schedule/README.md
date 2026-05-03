# 일정 관리 에이전트

## 목표

사용자가 대화로 일정을 알려주면 자동으로 정리·등록·알림까지 처리.
최소한의 노력으로 일정을 관리할 수 있게 한다.

## 핵심 기능 (예정)

- 자연어로 일정 전달 → 구조화해서 캘린더 등록
- Google Calendar 연동
- 일정 충돌 감지 및 조율 제안
- 일정 전 관련 자료 수집 → 리포트 생성
- 알림 발송

## 미결 사항

- [ ] 노트/문서 도구 선택: **Notion** vs **OneNote**
  - Notion: MCP 이미 연결됨, 단 무료 플랜
  - OneNote: MS365 구독 포함, OneDrive 1TB, Outlook 캘린더와 연동 유리
- [ ] 알림 채널 결정 (카카오톡, 이메일, 슬랙 등)
- [ ] Google Calendar OAuth 설정

## 스택 (미확정)

- Claude API
- Google Calendar API
- Notion API or Microsoft Graph API
