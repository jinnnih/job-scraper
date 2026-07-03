# 🔍 Job Scraper

> 한국 주요 구직 사이트를 매일 자동으로 수집하여 Gmail로 발송하는 개인 맞춤 구직 알림 도구

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=githubactions&logoColor=white)
![Gmail](https://img.shields.io/badge/Gmail_SMTP-EA4335?style=flat&logo=gmail&logoColor=white)

---

## 📬 실행 결과

매일 오전 9시, 아래와 같은 HTML 이메일이 자동 발송됩니다.

![이메일 예시](docs/email_preview.png)

---

## ✨ 주요 기능

- **4개 구직 사이트 자동 수집** — 사람인(공식 API), 원티드, 점핏, 잡코리아
- **키워드 필터링** — 관심 키워드 포함 공고만 추려서 발송
- **중복 제거** — 이미 발송된 공고는 재발송하지 않음 (`seen_jobs.json`)
- **HTML 이메일** — 사이트 출처 · 회사명 · 지역 · 링크 포함
- **완전 무료** — GitHub Actions 스케줄러 + Gmail SMTP

---

## 🛠 기술 스택

| 분류 | 기술 |
|------|------|
| Language | Python 3.11 |
| 크롤링 | `requests`, `BeautifulSoup4` |
| 이메일 발송 | `smtplib` (Python 내장), Gmail SMTP |
| 스케줄링 | GitHub Actions (`cron: '0 0 * * *'`) |
| 환경 변수 | `python-dotenv`, GitHub Secrets |
| API | 사람인 공식 REST API |

---

## 📁 프로젝트 구조

```
job-scraper/
├── scrapers/
│   ├── saramin.py      # 사람인 공식 API
│   ├── wanted.py       # 원티드 API v4
│   ├── jumpit.py       # 점핏 크롤링
│   └── jobkorea.py     # 잡코리아 크롤링
├── core/
│   ├── filter.py       # 키워드 필터링 + 중복 제거
│   └── mailer.py       # Gmail SMTP 발송
├── config.py           # 키워드 · 지역 · 설정
├── main.py             # 실행 진입점
├── seen_jobs.json      # 발송 완료 공고 ID 저장
└── .github/
    └── workflows/
        └── daily.yml   # GitHub Actions 스케줄러
```

---

## ⚙️ 설치 및 실행

### 1. 클론 및 의존성 설치

```bash
git clone https://github.com/jinnnih/job-scraper.git
cd job-scraper
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일을 열어 값 입력
```

```env
# 원하는 키워드를 콤마로 구분해서 입력
KEYWORDS=Python,백엔드,Django,AWS

# 제외할 키워드
EXCLUDE_KEYWORDS=경력 10년,수석,팀장

# 지역 설정
LOCATION_LABEL=수도권
SARAMIN_LOC_CD=R1,R2,R6

# Gmail 설정
SARAMIN_API_KEY=사람인_API_키
GMAIL_USER=발신_Gmail_주소
GMAIL_APP_PASSWORD=Gmail_앱_비밀번호_16자리
RECIPIENT_EMAIL=수신_Gmail_주소
```

> 키워드만 바꾸면 누구든 자신의 직군에 맞게 사용 가능합니다.

### 3. 로컬 실행

```bash
# 일반 실행 (신규 공고만 발송)
python3 main.py

# 테스트 모드 (seen_jobs 무시, 최신 5건 강제 발송)
python3 main.py --test
```

---

## 🔁 자동화 (GitHub Actions)

`.github/workflows/daily.yml`이 **매일 KST 09:00**에 자동 실행됩니다.

GitHub 레포 → **Settings → Secrets and variables → Actions** 에서 아래 4개 등록:

| Secret 이름 | 내용 |
|-------------|------|
| `SARAMIN_API_KEY` | 사람인 API 키 |
| `GMAIL_USER` | 발신 Gmail 주소 |
| `GMAIL_APP_PASSWORD` | Gmail 앱 비밀번호 |
| `RECIPIENT_EMAIL` | 수신 이메일 주소 |

수동 실행: **Actions 탭 → `매일 구직 공고 수집 및 발송` → Run workflow**

---

## 🔑 사전 준비

| 항목 | 발급 위치 |
|------|-----------|
| 사람인 API 키 | https://oapi.saramin.co.kr |
| Gmail 앱 비밀번호 | Google 계정 → 보안 → 앱 비밀번호 |

---

## 📊 무료 한도

| 구성요소 | 무료 한도 |
|----------|-----------|
| GitHub Actions | 월 2,000분 (하루 실행 약 1분 소요) |
| 사람인 API | 일 1,000회 |
| Gmail SMTP | 제한 없음 |
