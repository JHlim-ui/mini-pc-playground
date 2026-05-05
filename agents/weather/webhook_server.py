"""
카카오 챗봇 Webhook 서버
- 사용자가 카카오 채널에 메시지 보내면 이 서버가 받아서 명령 처리
- 카카오 챗봇 빌더 응답 형식(v2) 준수
"""
import os
import json
import threading
import logging
import requests
import anthropic
from flask import Flask, request, jsonify
import kakao_client

logger = logging.getLogger(__name__)
app = Flask(__name__)

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

HELP_TEXT = """사용 가능한 명령어:
• 날씨 - 강남구 내일 날씨
• 도움말 - 명령어 목록"""


def build_response(text: str) -> dict:
    """카카오 챗봇 응답 형식"""
    return {
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": text}}]
        }
    }


def handle_weather_command():
    """날씨 조회 후 나에게 보내기로 전달 (백그라운드)"""
    def _run():
        try:
            from main import get_weather, summarize_with_claude
            weather = get_weather()
            summary = summarize_with_claude(weather)
            kakao_client.send_to_me(f"강남구 내일 날씨\n\n{summary}")
        except Exception as e:
            logger.error(f"날씨 처리 오류: {e}")
    threading.Thread(target=_run, daemon=True).start()


def handle_claude_command(text: str) -> str:
    """Claude에게 자유 질문"""
    try:
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role": "user", "content": text}]
        )
        return msg.content[0].text
    except Exception as e:
        return f"Claude 오류: {e}"


@app.route("/kakao/webhook", methods=["POST"])
def kakao_webhook():
    data = request.get_json(silent=True) or {}
    utterance = data.get("userRequest", {}).get("utterance", "").strip()
    logger.info(f"카카오 명령 수신: {utterance}")

    if not utterance:
        return jsonify(build_response("명령어를 입력해주세요."))

    if "날씨" in utterance:
        handle_weather_command()
        return jsonify(build_response("날씨를 조회 중입니다. 잠시 후 카카오톡으로 전송됩니다!"))

    elif utterance in ("도움말", "help", "?"):
        return jsonify(build_response(HELP_TEXT))

    else:
        answer = handle_claude_command(utterance)
        return jsonify(build_response(answer))


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


def run_webhook(port=5000):
    logger.info(f"카카오 Webhook 서버 시작 (port {port})")
    app.run(host="0.0.0.0", port=port, debug=False)
