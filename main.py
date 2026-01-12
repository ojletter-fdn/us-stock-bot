import os
import requests
import google.generativeai as genai

# 1. 환경 변수에서 열쇠 꺼내기
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
NEWS_KEY = os.environ.get('NEWS_API_KEY')

def get_news():
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={NEWS_KEY}'
    r = requests.get(url).json()
    news_list = []
    if 'feed' in r:
        for item in r['feed'][:5]:
            news_list.append(f"제목: {item['title']}\n요약: {item['summary']}")
        return "\n\n".join(news_list)
    return None

def send_msg(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    response = requests.post(url, data={'chat_id': CHAT_ID, 'text': msg})
    # 아래 줄을 추가해서 전송 결과를 로그에 남겨보자
    print(f"전송 결과: {response.status_code}, {response.text}")
        
    prompt = f"""
    너는 15년 차 개인 투자자야. 말투는 짧고 단정하게, 반말 70% + 존댓말 30%를 섞어서 써줘. 
    아래 미국 증시 뉴스를 요약해줘.
    - 구성: 제목(후킹), 본문의 인사이트(관점), 내용(요약) 순서.
    - 제약: 500자 이내로 작성.
    - 톤: 확신보다는 확률을 말하고, 조용히 돈 버는 사람 느낌으로.
    
    뉴스 내용:
    {text}
    """
    response = model.generate_content(prompt)
    return response.text

def send_msg(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': msg})

# 실행
if __name__ == "__main__":
    news_data = get_news()
    if news_data:
        try:
            summary = summarize(news_data)
            send_msg(summary)
        except Exception as e:
            send_msg(f"요약 중 에러 발생: {str(e)}")
    else:
        send_msg("가져온 뉴스가 없어. 시장 휴장 여부를 확인해봐.")
