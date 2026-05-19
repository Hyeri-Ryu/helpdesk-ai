"""데모용 샘플 티켓 20건을 분류해서 DB에 저장.

사용법:
    python sample_data.py
"""
import random
from datetime import datetime, timedelta
from db import init_db, save_ticket, clear_tickets
from classifier import classify_ticket

SAMPLE_TICKETS = [
    "VPN 연결이 안 됩니다. 재택근무 중인데 사내 시스템 접속이 안 돼요.",
    "비밀번호를 잊어버렸습니다. 재설정 부탁드립니다.",
    "프린터에서 종이가 계속 걸려요. 토너 교체도 필요할 것 같습니다.",
    "Excel이 자꾸 멈춥니다. 최근 업데이트 이후로 발생하는 문제 같아요.",
    "Wi-Fi 신호가 약해서 화상 회의가 자꾸 끊깁니다. 긴급합니다.",
    "노트북이 아예 켜지지 않습니다. 어제까지 정상 동작했어요.",
    "Slack 로그인이 안 됩니다.",
    "Adobe 라이센스 인증은 어떻게 진행하나요?",
    "회의실 모니터 출력이 안 됩니다. 10분 뒤 미팅인데 급해요.",
    "이메일 첨부파일이 안 보내져요. 용량 제한이 어떻게 되나요?",
    "Windows 업데이트 후 부팅 속도가 매우 느려졌습니다.",
    "마우스가 갑자기 작동을 안 합니다. 무선 마우스인데 배터리는 충분합니다.",
    "사내 ERP 시스템 접속 권한 발급 요청드립니다.",
    "VS Code 설치 권한을 요청드립니다.",
    "사무실 인터넷이 전체적으로 느립니다. 우리 팀 전체가 같은 증상이에요.",
    "신규 입사자 계정 발급 부탁드립니다. 다음 주 월요일 출근 예정입니다.",
    "Zoom에서 카메라가 인식되지 않습니다.",
    "프린터 토너 교체 요청드립니다.",
    "GitHub 접속이 차단된 것 같아요. 외부 리포지토리 클론이 안 됩니다.",
    "MS Office가 자꾸 비활성화됩니다. 라이센스 문제일까요?",
]


def seed(clear: bool = True):
    init_db()
    if clear:
        clear_tickets()
        print("기존 티켓 데이터를 모두 삭제했습니다.")

    print(f"\n샘플 티켓 {len(SAMPLE_TICKETS)}건 분류 및 저장 중...\n")

    now = datetime.now()
    for i, text in enumerate(SAMPLE_TICKETS, 1):
        result = classify_ticket(text)
        # 최근 14일 사이 랜덤한 시점으로 분산
        days_ago = random.uniform(0, 14)
        created = (now - timedelta(days=days_ago)).isoformat(timespec="seconds")
        save_ticket(text, result, created_at=created)
        print(
            f"  [{i:2d}/{len(SAMPLE_TICKETS)}] "
            f"{result['category']:6s} | {result['priority']:3s} | "
            f"{text[:35]}..."
        )

    print("\n✅ 완료! 이제 `streamlit run app.py`로 대시보드를 확인하세요.")


if __name__ == "__main__":
    seed()
