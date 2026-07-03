"""구직 스크래퍼 메인 실행"""
import sys
from dotenv import load_dotenv
load_dotenv()

from scrapers import saramin, wanted, jumpit, jobkorea
from core import filter, mailer

def run(test_mode: bool = False):
    from config import KEYWORDS
    if not KEYWORDS:
        print("❌ KEYWORDS가 설정되지 않았습니다.")
        print("   .env 파일에 아래 형식으로 추가해주세요:")
        print("   KEYWORDS=Python,백엔드,Django")
        return

    print("🔍 구직 공고 수집 시작...")

    all_jobs = []
    all_jobs += saramin.fetch();  print(f"  사람인:   {len(all_jobs)}건")
    prev = len(all_jobs)
    all_jobs += wanted.fetch();   print(f"  원티드:   {len(all_jobs)-prev}건")
    prev = len(all_jobs)
    all_jobs += jumpit.fetch();   print(f"  점핏:     {len(all_jobs)-prev}건")
    prev = len(all_jobs)
    all_jobs += jobkorea.fetch(); print(f"  잡코리아: {len(all_jobs)-prev}건")

    print(f"\n총 수집: {len(all_jobs)}건")

    if test_mode:
        # 테스트 모드: seen_jobs 무시하고 최신 5건만 강제 발송
        filtered = all_jobs[:5]
        print(f"[테스트 모드] 상위 5건 강제 발송")
    else:
        filtered = filter.apply(all_jobs)
        print(f"필터 통과: {len(filtered)}건 (신규)")

    mailer.send(filtered)

if __name__ == "__main__":
    test_mode = "--test" in sys.argv
    run(test_mode=test_mode)
