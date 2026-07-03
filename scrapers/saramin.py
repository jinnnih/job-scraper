"""사람인 공식 API 스크래퍼"""
import requests
from config import SARAMIN_API_KEY, KEYWORDS, SARAMIN_LOC_CD

BASE_URL = "https://oapi.saramin.co.kr/job-search"

def fetch() -> list[dict]:
    if not SARAMIN_API_KEY:
        print("[사람인] API 키 없음 — 건너뜀")
        return []

    jobs = []
    for keyword in KEYWORDS[:5]:  # 상위 5개 키워드로 검색
        try:
            resp = requests.get(BASE_URL, params={
                "access-key": SARAMIN_API_KEY,
                "keywords":   keyword,
                "loc_cd":     SARAMIN_LOC_CD,
                "job_mid_cd": "2",   # IT/인터넷/통신
                "count":      "40",
                "sr":         "directhire",
            }, timeout=10)
            data = resp.json()
            for job in data.get("jobs", {}).get("job", []):
                jobs.append({
                    "id":      f"saramin_{job['id']}",
                    "source":  "사람인",
                    "title":   job["position"]["title"],
                    "company": job["company"]["detail"]["name"],
                    "location":job["position"]["location"]["name"],
                    "url":     job["url"],
                })
        except Exception as e:
            print(f"[사람인] 오류: {e}")

    # 중복 제거
    seen = set()
    unique = []
    for j in jobs:
        if j["id"] not in seen:
            seen.add(j["id"])
            unique.append(j)
    return unique
