# 🎫 IT 헬프데스크 자동 분류 시스템

## AI 기반 IT 헬프데스크 티켓 자동 분류·1차 응답·BI 대시보드를 통합한 사내 자동화 도구.

## 🎯 직무 적합성 매핑

| 프로젝트 구현 |
| 스크립트 / RPA 솔루션 | Python으로 반복 분류 업무 자동화 |
| AI Transformation (AX) | Claude API 기반 자연어 분류·요약·응답 생성 |
| 인프라 관리 효율화 | 헬프데스크 응답 시간 단축, 우선순위 자동 분류 |
| BI 도구 / 디지털화 | Plotly 대시보드, KPI, 시간대별 추이 시각화 |
| 프로세스 문서화 | 자주 묻는 유형 자동 분류 → 지식베이스 축적 가능 |

---

## ✨ 주요 기능

1. **AI 자동 분류** — 자연어 문의를 카테고리/우선순위로 자동 분류
2. **1차 자동 응답** — 자주 묻는 유형은 즉시 템플릿 응답 제공
3. **담당자 라우팅** — 복잡한 문제는 담당자 배정 플래그 자동 부여
4. **BI 대시보드** — 카테고리별·우선순위별·시간대별 분포 시각화
5. **CSV 내보내기** — 필터링된 티켓 데이터 다운로드
6. **API 키 없어도 동작** — 룰 기반 폴백으로 즉시 데모 가능

---

## 🛠 기술 스택

- **Python 3.10+**
- **Streamlit** — 데이터/내부 도구용 웹 UI 프레임워크
- **Anthropic Claude API** — 자연어 분류·요약 (haiku-4-5)
- **SQLite** — 경량 임베디드 DB
- **Plotly** — 인터랙티브 차트
- **Pandas** — 데이터 집계

---

## 🚀 빠른 시작

### 1) 환경 설정

```bash
# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2) (선택) AI 모드 활성화

```bash
cp .env.example .env
# .env 파일 열어서 ANTHROPIC_API_KEY 입력
```

> 키를 설정하지 않아도 룰 기반 모드로 즉시 동작합니다.

### 3) 샘플 데이터 생성 (선택)

```bash
python sample_data.py
```

샘플 티켓 20건을 자동 분류하여 DB에 저장합니다. 대시보드를 바로 보고 싶을 때 사용.

### 4) 앱 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 자동 오픈.

---

## 📁 프로젝트 구조

```
helpdesk-ai/
├── app.py              # Streamlit 메인 (입력 폼 + 대시보드 + 목록)
├── classifier.py       # AI 분류 + 룰 기반 폴백
├── db.py               # SQLite 저장/조회
├── templates.py        # 카테고리별 자동 응답 템플릿
├── sample_data.py      # 데모 시드 스크립트
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 인터뷰용 30초 피치

> "IT 헬프데스크에서 반복적으로 발생하는 단순 문의(VPN, 비밀번호, 프린터 등)가
> 담당자의 시간을 많이 소모한다는 문제에 주목해, **LLM 기반 자동 분류 + 1차 응답
> 시스템**을 구축했습니다. Python으로 분류 로직과 SQLite 데이터 파이프라인을
> 만들고, Streamlit으로 사내 도구 UI를, Plotly로 BI 대시보드를 구현했습니다.
> API 비용 부담 없이 누구나 즉시 데모할 수 있도록 키워드 기반 폴백 모드도
> 함께 설계했습니다."

---

## 📜 License

MIT
