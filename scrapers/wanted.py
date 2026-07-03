"""원티드 API v4 스크래퍼"""
import requests
from config import KEYWORDS

BASE_URL = "https://www.wanted.co.kr/api/v4/jobs"
HEADERS = {
    "User-Agent":        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Referer":           "https://www.wanted.co.kr",
    "x-wanted-language": "ko",
}

def fetch() -> list[dict]:
    jobs = []
    for keyword in KEYWORDS[:5]:
        try:
            resp = requests.get(BASE_URL, params={
                "query":    keyword,
                "country":  "kr",
                "job_sort": "job.latest_order",
                "limit":    20,
            }, headers=HEADERS, timeout=10)

            if resp.status_code != 200:
                continue

            for job in resp.json().get("data", []):
                jobs.append({
                    "id":      f"wanted_{job['id']}",
                    "source":  "원티드",
                    "title":   job.get("position", ""),
                    "company": job.get("company", {}).get("name", ""),
                    "location":job.get("address", {}).get("location", ""),
                    "url":     f"https://www.wanted.co.kr/wd/{job['id']}",
                })
        except Exception as e:
            print(f"[원티드] 오류: {e}")

    seen = set()
    unique = [j for j in jobs if not (j["id"] in seen or seen.add(j["id"]))]
    return unique
