"""카카오 API 클라이언트 - 토큰 관리 + 나에게 보내기"""
import os
import json
import requests
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

TOKEN_URL  = "https://kauth.kakao.com/oauth/token"
SEND_URL   = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
TOKEN_FILE = Path("/app/data/kakao_token.json")

REST_API_KEY  = os.getenv("KAKAO_REST_API_KEY")
REDIRECT_URI  = os.getenv("KAKAO_REDIRECT_URI", "http://localhost:5000/kakao/callback")


def load_tokens():
    if TOKEN_FILE.exists():
        return json.loads(TOKEN_FILE.read_text())
    raise FileNotFoundError("토큰 없음. scripts/kakao_auth.py 실행해서 최초 인증 필요")


def save_tokens(tokens: dict):
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(json.dumps(tokens, indent=2))


def refresh_access_token() -> str:
    tokens = load_tokens()
    r = requests.post(TOKEN_URL, data={
        "grant_type":    "refresh_token",
        "client_id":     REST_API_KEY,
        "refresh_token": tokens["refresh_token"],
    }, timeout=10)
    r.raise_for_status()
    new = r.json()
    if "refresh_token" not in new:          # 갱신 안 된 경우 기존 유지
        new["refresh_token"] = tokens["refresh_token"]
    save_tokens(new)
    logger.info("카카오 액세스 토큰 갱신 완료")
    return new["access_token"]


def send_to_me(text: str):
    """나에게 보내기"""
    access_token = refresh_access_token()
    template = {
        "object_type": "text",
        "text": text[:500],           # 카카오 제한
        "link": {"web_url": "", "mobile_web_url": ""}
    }
    r = requests.post(SEND_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        data={"template_object": json.dumps(template, ensure_ascii=False)},
        timeout=10
    )
    r.raise_for_status()
    logger.info("카카오 메시지 전송 완료")
    return r.json()
