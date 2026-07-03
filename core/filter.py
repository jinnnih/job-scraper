"""키워드 필터링 + 중복 제거"""
import json
import os
from config import KEYWORDS, EXCLUDE_KEYWORDS

SEEN_FILE = os.path.join(os.path.dirname(__file__), "../seen_jobs.json")

def _load_seen() -> set:
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()

def _save_seen(seen: set):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)

def apply(jobs: list[dict]) -> list[dict]:
    """키워드 필터 → 제외어 필터 → 중복(seen) 제거"""
    seen = _load_seen()
    result = []

    for job in jobs:
        text = f"{job['title']} {job['company']}".lower()

        # 제외 키워드 포함 시 스킵
        if any(ex.lower() in text for ex in EXCLUDE_KEYWORDS):
            continue

        # 매칭 키워드 없으면 스킵
        if not any(kw.lower() in text for kw in KEYWORDS):
            continue

        # 이미 발송된 공고 스킵
        if job["id"] in seen:
            continue

        result.append(job)

    # 새로 수집된 공고 ID 저장
    new_ids = {j["id"] for j in result}
    _save_seen(seen | new_ids)

    return result
