"""
강남구 날씨 에이전트
- 매일 오전 7시에 내일 날씨를 Claude Haiku로 요약해서 텔레그램으로 전송
"""
import os
import schedule
import time
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
TELEGRAM_BOT_TOKEN  = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID    = os.getenv("TELEGRAM_CHAT_ID")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

GANGNAM_LAT = 37.5172
GANGNAM_LON = 127.0473


def get_weather():
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": GANGNAM_LAT,
        "lon": GANGNAM_LON,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "kr",
        "cnt": 8,
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()


def summarize_with_claude(weather_data):
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    items = weather_data["list"][:8]
    forecast_lines = [
        f"{item['dt_txt'][11:16]} - {item['main']['temp']:.0f}C "
        f"({item['weather'][0]['description']}), "
        f"습도 {item['main']['humidity']}%, "
        f"체감 {item['main']['feels_like']:.0f}C"
        for item in items
    ]
    forecast_text = "\n".join(forecast_lines)
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        messages=[{
            "role": "user",
            "content": (
                f"서울 강남구 내일 날씨 데이터:\n{forecast_text}\n\n"
                "3줄 이내로 친근하게 요약하고 최저/최고 기온, 옷차림 추천 포함. "
                "이모지 사용해서 텔레그램 메시지로."
            )
        }]
    )
    return msg.content[0].text


def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    r = requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }, timeout=10)
    r.raise_for_status()


def run_weather_report():
    logger.info("날씨 리포트 시작")
    try:
        weather = get_weather()
        summary = summarize_with_claude(weather)
        send_telegram(f"*강남구 내일 날씨*\n\n{summary}")
        logger.info("텔레그램 전송 완료")
    except Exception as e:
        logger.error(f"오류: {e}", exc_info=True)


def main():
    logger.info("날씨 에이전트 시작 - 매일 07:00 실행")
    schedule.every().day.at("07:00").do(run_weather_report)
    run_weather_report()  # 시작 시 즉시 한 번 실행
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
