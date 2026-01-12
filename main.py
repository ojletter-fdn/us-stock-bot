import os
import requests
from openai import OpenAI

# 1. 환경 변수에서 키 가져오기
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
OPENAI_KEY = os.environ['OPENAI_API_KEY']
NEWS_KEY = os.environ['NEWS_API_KEY']

# OpenAI 클라이언트 설정
client = OpenAI(api_key=OPENAI_KEY)

def get_news():
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={NEWS_KEY}'
    r = requests.get(url).json()
    news_list = []
    # 뉴스 데이터가 있는지 확인
    if 'feed' in r:
        for item in r['feed'][:5]:
            news_list.append(f"제목: {item['title']}\n요약: {item['summary']}")
        return "\n\n".join(news_list)
    return None

def summarize(text):
    # GPT-4o 모델 사용 (유료 사용자라면 매우 빠르고 정확함)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 15년차 개인 투자자야. 말투는 짧고 단정하게, 반말 70% + 존댓말 30%를 섞어서 써줘. 정답을 맞히기보다 확률을 줄여주는 관점에서 분석해."},
            {"role": "user", "content": f"다음 미국 뉴스를 스레드 스타일(제목 후킹, 인사이트, 내용 요약)로 500자 이내 요약해줘:\n\n{text}"}
        ]
    )
    return response.choices[0].message.content

def send_msg(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': msg})

# 실행
news_data = get_news()
if news_data:
    summary = summarize(news_data)
    send_msg(summary)
else:
    send_msg("가져온 뉴스가 없어. API 키나 시장 휴장 여부를 확인해봐.")
