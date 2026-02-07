#========================================================================
# 네이버에서 뉴스를 검색해 헤드라인 15개를 가져오는 스크립트
# 수집한 헤드라인은 날짜별로 폴더를 생성해 csv 파일로 저장 및 워드 클라우드 생성
#========================================================================
# 내장 라이브러리
from datetime import datetime
import csv
import time
import os

# 외부 라이브러리
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# 네이버 뉴스 url
# 정치 "https://news.naver.com/section/100"
# 경제 "https://news.naver.com/section/101"
# 사회 "https://news.naver.com/section/102" 
# 생활 문화 "https://news.naver.com/section/103"
# 세계 "https://news.naver.com/section/104"
# IT/과학 "https://news.naver.com/section/105"


# 1.뉴스 선택
def get_section_url():
    url_map = {
        1: "100",
        2: "101",
        3: "102",
        4: "103",
        5: "104",
        6: "105"
    }

    print("원하는 뉴스의 번호를 선택하세요")
    print("""
        1 : 정치
        2 : 경제
        3 : 사회
        4 : 생활 문화
        5 : 세계
        6 : IT/과학 """)

    while True:
        try:
            choice = int(input("뉴스 번호 입력 (1~6): "))
            if choice in url_map:
                return f"https://news.naver.com/section/{url_map[choice]}"
            else:
                print("1~6 사이 숫자 입력")
        except ValueError:
            print("숫자만 입력")



# 2.뉴스 헤드라인 수집
def collect_news(url):
    headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
    # 웹사이트에 페이지 요청
    response = requests.get(url, headers=headers, timeout=10)

    titles = []

    # 상태 코드가 200(연결 성공)이면 다음 단계 진행
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        headlines = soup.select(".sa_text_title")[:15] # 헤드라인 15개 가져오기

        current_time = datetime.now().strftime("%Y%m%d_%H%M")
        print(f"[{current_time}] 뉴스 헤드라인\n")

        for h in headlines:
            title = h.get_text().strip()
            titles.append(title)
    else:
        print("뉴스 수집 실패" , response.status_code)
        return []

    titles = list(dict.fromkeys(titles))
    return titles



# 3. 워드클라우드 생성
def create_wordcloud(text):
    now = datetime.now()

    wc = WordCloud(
        font_path="malgun.ttf",  # 한글 폰트 (Windows)
        # font_path='/System/Library/Fonts/AppleGothic.ttf',  # Mac
        # font_path='/usr/share/fonts/truetype/nanum/NanumGothic.ttf',  # Linux
        width=850,
        height=600,
        max_words=250,  # 최대 단어 수
        max_font_size=120,
        background_color="white"
    ).generate(text)

    date_folder = now.strftime("%Y-%m-%d")
    filename = now.strftime("%H%M")
    filepath = os.path.join(date_folder, f"wordcloud{filename}.png")

    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(filepath, dpi=300)
    plt.show()


# csv 파일로 저장
def save_to_csv(titles):
    now = datetime.now()

    # 날짜 폴더
    date_folder = now.strftime("%Y-%m-%d")
    os.makedirs(date_folder, exist_ok=True)

    # 파일명 (시간)
    filename = now.strftime("%H%M")
    filepath = os.path.join(date_folder, f"news_{filename}.csv")

    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["헤드라인"])

        for title in titles:
            writer.writerow([title])

    print(f"{filepath} 저장 완료")

# 4. 실행
def main(url):
    
    titles = collect_news(url)

    save_to_csv(titles)
    text = " ".join(titles)
    print(text)

    if titles:
        create_wordcloud(text)
    else:
        print("수집 된 뉴스 없음")


if __name__ == "__main__":
    # 2 시간마다 자동으로 뉴스 수집
    url = get_section_url()
    try:
        while True: 
            try:
                main(url)
            except Exception as e:
                print("에러 발생", e)
            time.sleep(7200)
    except KeyboardInterrupt:
        print("\n=================================")
        print(" 프로그램을 안전하게 종료합니다")
        print("=================================")
    
