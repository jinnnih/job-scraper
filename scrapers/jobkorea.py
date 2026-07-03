"""잡코리아 HTML 크롤링 스크래퍼"""
import requests
from bs4 import BeautifulSoup
from config import KEYWORDS

BASE_URL = "https://www.jobkorea.co.kr/Search/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9",
}

def fetch() -> list[dict]:
    jobs = []
    for keyword in KEYWORDS[:3]:
        try:
            resp = requests.get(BASE_URL, params={
                "stext": keyword,
                "local": "101000,102000,106000",  # 서울·경기·인천
            }, headers=HEADERS, timeout=10)

            soup = BeautifulSoup(resp.text, "html.parser")
            cards = soup.select("div.list-section article.list-item")

            for card in cards[:20]:
                title_el   = card.select_one("a.title")
                company_el = card.select_one("a.name")
                loc_el     = card.select_one("span.option-item")
                href       = title_el["href"] if title_el and title_el.get("href") else ""
                job_id     = href.split("Recruit/View?rNo=")[-1].split("&")[0] if "rNo=" in href else href

                if not title_el:
                    continue

                jobs.append({
                    "id":      f"jobkorea_{job_id}",
                    "source":  "잡코리아",
                    "title":   title_el.get_text(strip=True),
                    "company": company_el.get_text(strip=True) if company_el else "",
                    "location":loc_el.get_text(strip=True) if loc_el else "",
                    "url":     f"https://www.jobkorea.co.kr{href}" if href.startswith("/") else href,
                })
        except Exception as e:
            print(f"[잡코리아] 오류: {e}")

    seen = set()
    unique = []
    for j in jobs:
        if j["id"] not in seen:
            seen.add(j["id"])
            unique.append(j)
    return unique
