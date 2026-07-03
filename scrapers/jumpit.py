"""점핏 HTML 크롤링 스크래퍼"""
import requests
from bs4 import BeautifulSoup
from config import KEYWORDS

BASE_URL = "https://www.jumpit.co.kr/search"
HEADERS = {
    "User-Agent":      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9",
}

def fetch() -> list[dict]:
    jobs = []
    for keyword in KEYWORDS[:4]:
        try:
            resp = requests.get(BASE_URL, params={"keyword": keyword},
                                headers=HEADERS, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")

            # 점핏 공고 카드 파싱
            for card in soup.select("a[href*='/position/']")[:15]:
                href    = card.get("href", "")
                pos_id  = href.split("/position/")[-1].split("?")[0]
                title   = card.select_one("h2, h3, .position_card_info_title")
                company = card.select_one(".company_name, .position_card_info_company")

                if not title:
                    continue

                jobs.append({
                    "id":      f"jumpit_{pos_id}",
                    "source":  "점핏",
                    "title":   title.get_text(strip=True),
                    "company": company.get_text(strip=True) if company else "",
                    "location":"",
                    "url":     f"https://www.jumpit.co.kr{href}" if href.startswith("/") else href,
                })
        except Exception as e:
            print(f"[점핏] 오류: {e}")

    seen = set()
    unique = [j for j in jobs if not (j["id"] in seen or seen.add(j["id"]))]
    return unique
