"""
카카오 최초 OAuth 인증 스크립트 (1회만 실행)

사용법:
  1. .env 파일에 KAKAO_REST_API_KEY 설정
  2. 카카오 개발자 앱 > 플랫폼 > Web에 http://localhost:5000 등록
  3. 카카오 개발자 앱 > 카카오 로그인 > Redirect URI에 http://localhost:5000/kakao/callback 등록
  4. python scripts/kakao_auth.py 실행 → 브라우저 URL 복사
  5. 나온 URL을 브라우저에서 열고 카카오 로그인
  6. 리다이렉트된 URL에서 code= 파라미터 값 복사해서 터미널에 붙여넣기
  7. data/kakao_token.json 생성 확인 → docker compose up
"""
import os
import sys
import json
import requests
from pathlib import Path
from urllib.parse import urlencode

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI", "http://localhost:5000/kakao/callback")
TOKEN_FILE   = Path("data/kakao_token.json")


def main():
    if not REST_API_KEY:
        print("[오류] KAKAO_REST_API_KEY 환경변수가 없습니다. .env 파일을 확인하세요.")
        sys.exit(1)

    # Step 1: 인증 URL 출력
    params = urlencode({
        "client_id":     REST_API_KEY,
        "redirect_uri":  REDIRECT_URI,
        "response_type": "code",
        "scope":         "talk_message",
    })
    auth_url = f"https://kauth.kakao.com/oauth/authorize?{params}"
    print("\n아래 URL을 브라우저에서 열고 카카오 로그인 후")
    print("리다이렉트된 URL에서 code= 값을 복사하세요:\n")
    print(auth_url)
    print()

    # Step 2: code 입력받기
    code = input("code 값 입력: ").strip()
    if not code:
        print("code가 비어있습니다.")
        sys.exit(1)

    # Step 3: 토큰 발급
    r = requests.post("https://kauth.kakao.com/oauth/token", data={
        "grant_type":   "authorization_code",
        "client_id":    REST_API_KEY,
        "redirect_uri": REDIRECT_URI,
        "code":         code,
    }, timeout=10)

    if r.status_code != 200:
        print(f"[오류] 토큰 발급 실패: {r.text}")
        sys.exit(1)

    tokens = r.json()
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(json.dumps(tokens, indent=2))
    print(f"\n토큰 저장 완료: {TOKEN_FILE}")
    print("이제 docker compose up -d 를 실행하세요.")


if __name__ == "__main__":
    main()
