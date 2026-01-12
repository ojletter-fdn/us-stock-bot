import os
import requests
import google.generativeai as genai

# 1. 환경 변수에서 키 가져오기
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
GEMINI_KEY = os.environ['GEMINI_API_KEY']
NEWS_KEY = os.environ['NEWS_API_KEY']

def get_news():
    # 미국 주요 주식 뉴스 5개 가져오기
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={NEWS_KEY}'
    r = requests.get(url).json()
    news_list = []
    for item in r.get('feed', [])[:5]:
        news_list.append(f"제목: {item['title']}\n요약: {item['summary']}")
    return "\n\n".join(news_list)

def summarize(text):
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"너는 15년차 투자자야. 다음 뉴스를 스레드 스타일로 요약해줘. 제목(후킹), 인사이트, 내용 순으로 작성하고 500자 이내로 해. 반말과 존댓말을 섞어서 담백하게 써줘.\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

def send_msg(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': msg})

# 실행
news_data = get_news()
if news_data:
    summary = summarize(news_data)
    send_msg(summary)
else:
    send_msg("오늘은 가져올 뉴스가 없네. 휴장일인지 확인해봐.")
