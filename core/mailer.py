"""Gmail SMTP 발송"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from config import GMAIL_USER, GMAIL_APP_PASSWORD, RECIPIENT_EMAIL

def send(jobs: list[dict]):
    if not jobs:
        print("발송할 공고 없음")
        return

    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("[메일] Gmail 설정 없음 — 터미널에 결과 출력")
        _print_jobs(jobs)
        return

    today = datetime.now().strftime("%Y년 %m월 %d일")
    subject = f"[구직 알림] {today} 새 공고 {len(jobs)}건"

    # HTML 이메일 본문
    rows = ""
    for job in jobs:
        rows += f"""
        <tr>
          <td style="padding:12px;border-bottom:1px solid #eee;">
            <span style="background:#e8f4fd;color:#1a73e8;font-size:11px;
                         padding:2px 8px;border-radius:10px;font-weight:600;">
              {job['source']}
            </span>
            &nbsp;
            <a href="{job['url']}" style="font-size:15px;font-weight:600;
                                          color:#202124;text-decoration:none;">
              {job['title']}
            </a>
            <br/>
            <span style="font-size:13px;color:#5f6368;">
              {job['company']} &nbsp;|&nbsp; {job['location']}
            </span>
          </td>
        </tr>"""

    html = f"""
    <html><body style="font-family:sans-serif;background:#f8f9fa;padding:20px;">
      <div style="max-width:640px;margin:0 auto;background:#fff;
                  border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.1);">
        <div style="background:#1a73e8;padding:20px 24px;">
          <h2 style="color:#fff;margin:0;">🔍 오늘의 맞춤 구직 공고</h2>
          <p style="color:#c5deff;margin:4px 0 0;">{today} · {len(jobs)}건 수집</p>
        </div>
        <table style="width:100%;border-collapse:collapse;">
          {rows}
        </table>
        <div style="padding:16px 24px;color:#9aa0a6;font-size:12px;">
          사람인 · 원티드 · 점핏 · 잡코리아 자동 수집 | 매일 오전 9시 발송
        </div>
      </div>
    </body></html>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = GMAIL_USER
    msg["To"]      = RECIPIENT_EMAIL
    msg.attach(MIMEText(html, "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, RECIPIENT_EMAIL, msg.as_string())
        print(f"✅ 이메일 발송 완료 → {RECIPIENT_EMAIL} ({len(jobs)}건)")
    except Exception as e:
        print(f"❌ 이메일 발송 실패: {e}")
        _print_jobs(jobs)

def _print_jobs(jobs: list[dict]):
    """Gmail 설정 없을 때 터미널 출력"""
    print(f"\n{'='*60}")
    print(f"수집된 공고 {len(jobs)}건")
    print(f"{'='*60}")
    for job in jobs:
        print(f"[{job['source']}] {job['title']} | {job['company']} | {job['location']}")
        print(f"  👉 {job['url']}")
    print(f"{'='*60}\n")
