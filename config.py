"""구직 스크래퍼 설정 — .env 파일로 모든 설정 관리"""
import os

def _parse_list(env_key: str, default: list[str]) -> list[str]:
    """환경변수에서 콤마 구분 리스트 파싱"""
    raw = os.getenv(env_key, '')
    if raw.strip():
        return [k.strip() for k in raw.split(',') if k.strip()]
    return default

# ── 검색 키워드 (.env의 KEYWORDS 또는 기본값) ─────────────────
KEYWORDS = _parse_list('KEYWORDS', [
    'Python', '개발자', '백엔드', '프론트엔드', '풀스택',
])

# ── 제외 키워드 (.env의 EXCLUDE_KEYWORDS 또는 기본값) ─────────
EXCLUDE_KEYWORDS = _parse_list('EXCLUDE_KEYWORDS', [
    '경력 10년', '시니어', '팀장', '수석',
])

# ── 지역 ──────────────────────────────────────────────────────
LOCATION_LABEL = os.getenv('LOCATION_LABEL', '전국')
SARAMIN_LOC_CD  = os.getenv('SARAMIN_LOC_CD', '')  # 빈값이면 전국

# ── API 키 / 계정 ─────────────────────────────────────────────
SARAMIN_API_KEY    = os.getenv('SARAMIN_API_KEY', '')
GMAIL_USER         = os.getenv('GMAIL_USER', '')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD', '')
RECIPIENT_EMAIL    = os.getenv('RECIPIENT_EMAIL', GMAIL_USER)
