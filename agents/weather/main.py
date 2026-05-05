"""
강남구 날씨 에이전트 (카카오톡 버전)
- 매일 07:00 날씨 → 카카오 나에게 보내기
- Webhook 서버로 카카오 채널 명령 수신
"""
import os
import schedule
import time
import threading
import requests
import anthropic
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/app/logs/weather.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

CLAUDE_API_KEY      = os.getenv("CLAUDE_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
GANGNAM_LAT, GANGNAM_LON = 37.5172, 127.0473


def get_weather() -> dict:
    r = requests.get(
        "https://api.openweathermap.org/data/2.5/forecast",
        params={
            "lat": GANGNAM_LAT, "lon": GANGNAM_LON,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric", "lang": "kr", "cnt": 8,
        }, timeout=10
    )
    r.raise_for_status()
    return r.json()


def summarize_with_claude(weather_data: dict) -> str:
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    lines = [
        f"{i['dt_txt'][11:16]} {i['main']['temp']:.0f}C "
        f"({i['weather'][0]['description']}) 습도{i['main']['humidity']}%"
        for i in weather_data["list"][:8]
    ]
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        messages=[{"role": "user", "content":
            "강남구 내일 날씨:\n" + "\n".join(lines) +
            "\n\n3줄 이내로 친근하게 요약, 최저/최고 기온, 옷차림 추천, 이모지 포함."
        }]
    )
    return msg.content[0].text


def run_weather_report():
    import kakao_client
    logger.info("날씨 리포트 시작")
    try:
        weather = get_weather()
        summary = summarize_with_claude(weather)
        kakao_client.send_to_me(f"강남구 내일 날씨\n\n{summary}")
        logger.info("카카오 전송 완료")
    except Exception as e:
        logger.error(f"오류: {e}", exc_info=True)


def main():
    logger.info("날씨 에이전트 시작 - 매일 07:00 + 카카오 Webhook 수신")

    from webhook_server import run_webhook
    threading.Thread(target=run_webhook, args=(5000,), daemon=True).start()

    schedule.every().day.at("07:00").do(run_weather_report)

    run_weather_report()

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
