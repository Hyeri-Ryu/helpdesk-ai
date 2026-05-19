"""IT 헬프데스크 티켓 AI 분류기

- ANTHROPIC_API_KEY 환경변수가 설정되어 있으면 Claude API 사용
- 미설정 시 룰 기반 키워드 분류로 자동 폴백
"""
import os
import json
import re
from templates import AUTO_REPLIES

CATEGORIES = ["네트워크", "계정", "하드웨어", "소프트웨어", "기타"]
PRIORITIES = ["긴급", "보통", "낮음"]


def classify_with_ai(text: str) -> dict:
    """Claude API를 사용한 분류"""
    from anthropic import Anthropic

    client = Anthropic()

    prompt = f"""다음 IT 헬프데스크 문의를 분석해서 JSON 형식으로만 답하세요.
설명, 마크다운, 코드블록 없이 순수 JSON 객체만 출력하세요.

문의: {text}

출력 형식:
{{
  "category": "네트워크 | 계정 | 하드웨어 | 소프트웨어 | 기타 중 하나",
  "priority": "긴급 | 보통 | 낮음 중 하나",
  "summary": "한 문장으로 요약",
  "auto_reply": "자주 묻는 유형이면 1차 응답 메시지, 복잡한 문제면 빈 문자열",
  "needs_human": true 또는 false (담당자 배정 필요 여부)
}}"""

    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = msg.content[0].text.strip()
    # JSON 추출 (혹시 모르는 마크다운 제거)
    raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.MULTILINE).strip()
    return json.loads(raw)


def classify_with_rules(text: str) -> dict:
    """API 키 없을 때 사용하는 키워드 기반 폴백 분류"""
    text_lower = text.lower()

    keywords = {
        "네트워크": ["vpn", "와이파이", "wifi", "인터넷", "네트워크", "접속", "끊", "느려", "차단"],
        "계정": ["비밀번호", "패스워드", "로그인", "계정", "권한", "잠금", "발급", "초기화"],
        "하드웨어": ["프린터", "모니터", "키보드", "마우스", "노트북", "고장", "토너", "카메라", "안 켜"],
        "소프트웨어": ["설치", "프로그램", "오류", "에러", "업데이트", "라이센스", "excel", "office", "slack", "zoom", "ide"],
    }

    category = "기타"
    for cat, kws in keywords.items():
        if any(kw in text_lower for kw in kws):
            category = cat
            break

    urgent_kws = ["긴급", "급해", "급함", "바로", "asap", "당장", "안돼", "안 돼", "10분", "회의"]
    low_kws = ["문의", "어떻게", "방법"]
    if any(kw in text_lower for kw in urgent_kws):
        priority = "긴급"
    elif any(kw in text_lower for kw in low_kws):
        priority = "낮음"
    else:
        priority = "보통"

    auto_reply = AUTO_REPLIES.get(category, "")

    return {
        "category": category,
        "priority": priority,
        "summary": text[:60] + ("..." if len(text) > 60 else ""),
        "auto_reply": auto_reply,
        "needs_human": priority == "긴급" or not auto_reply,
    }


def classify_ticket(text: str) -> dict:
    """메인 분류 함수: API 키 있으면 AI, 없으면 룰 기반"""
    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            result = classify_with_ai(text)
            # AI가 auto_reply 빈 문자열로 응답해도 템플릿 채워주기
            if not result.get("auto_reply") and result.get("category") in AUTO_REPLIES:
                if AUTO_REPLIES[result["category"]]:
                    result["auto_reply"] = AUTO_REPLIES[result["category"]]
            return result
        except Exception as e:
            print(f"[WARN] AI 분류 실패, 룰 기반으로 폴백: {e}")
            return classify_with_rules(text)
    return classify_with_rules(text)
