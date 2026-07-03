"""구직 스크래퍼 설정 — 키워드·지역·이메일을 여기서 관리"""
import os

# ── 검색 키워드 (하나라도 포함되면 공고 수집) ──────────────────
KEYWORDS = [
    'ROS', 'ROS2', '자율주행', 'OpenCV', '로봇', '임베디드',
    '라즈베리파이', '라즈베리', '영상처리', '라이다', 'SLAM',
    '일본어', 'JLPT', '일본계', '센서', '모빌리티',
    'Python', 'C언어', '머신러닝', '딥러닝', '안드로이드',
]

# ── 제외 키워드 (포함되면 공고 필터링) ────────────────────────
EXCLUDE_KEYWORDS = [
    '경력 5년 이상', '경력 7년', '경력 10년', '시니어',
    '팀장', '리드', '수석',
]

# ── 지역 (사람인 지역코드, 크롤링 키워드 공통) ────────────────
LOCATION_LABEL = '수도권'          # 이메일 표시용
SARAMIN_LOC_CD  = 'R1,R2,R6,R13'  # 서울·경기·인천·경기남부

# ── API 키 / 계정 (환경변수 또는 .env에서 읽음) ───────────────
SARAMIN_API_KEY   = os.getenv('SARAMIN_API_KEY', '')
GMAIL_USER        = os.getenv('GMAIL_USER', '')
GMAIL_APP_PASSWORD= os.getenv('GMAIL_APP_PASSWORD', '')
RECIPIENT_EMAIL   = os.getenv('RECIPIENT_EMAIL', GMAIL_USER)
