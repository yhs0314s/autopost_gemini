import yfinance as yf
import requests
import random
import datetime
import os

def get_stock_data():
    # S&P 500(^GSPC)과 나스닥(^IXIC) 데이터 수집
    indices = {"S&P 500": "^GSPC", "나스닥": "^IXIC"}
    result = []
    for name, ticker in indices.items():
        data = yf.Ticker(ticker).history(period="2d")
        change = ((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100
        result.append({"name": name, "price": round(data['Close'].iloc[-1], 2), "change": round(change, 2)})
    return result

def generate_content(data):
    # AI 필터링 회피를 위한 문장 변주 (템플릿)
    intro_samples = [
        "간밤 뉴욕 증시는 엇갈린 행보를 보였습니다.",
        "오늘 아침 마감된 미 증시 요약해 드립니다.",
        "미국 시장이 마감되었습니다. 주요 지수 변동 사항입니다."
    ]
    
    content = f"## {random.choice(intro_samples)}\n\n"
    for item in data:
        status = "상승" if item['change'] > 0 else "하락"
        content += f"* **{item['name']}**: {item['price']} ({item['change']}% {status})\n"
    
    content += "\n\n구체적인 시황은 경제 지표 발표에 따라 변동성이 컸습니다. 성투하세요!"
    return content

def post_tistory(title, content):
    # 티스토리 API 설정
    url = "https://www.tistory.com/apis/post/write"
    params = {
        "access_token": os.environ['TISTORY_ACCESS_TOKEN'],
        "blogName": os.environ['TISTORY_BLOG_NAME'], # 티스토리 주소 앞부분
        "title": title,
        "content": content,
        "visibility": 3, # 3: 발행, 0: 비공개
        "category": "0",
        "output": "json"
    }
    res = requests.post(url, data=params)
    return res.json()

if __name__ == "__main__":
    stock_info = get_stock_data()
    post_title = f"[{datetime.date.today()}] 미국 증시 마감 시황 리포트"
    post_body = generate_content(stock_info)
    
    # 실제 발행
    response = post_tistory(post_title, post_body)
    print(f"Post Result: {response}")
