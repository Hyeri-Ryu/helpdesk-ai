"""IT 헬프데스크 자동 분류 시스템 - Streamlit UI

실행:
    streamlit run app.py
"""
import os
import streamlit as st
import plotly.express as px
import pandas as pd

from classifier import classify_ticket
from db import save_ticket, load_all_tickets, clear_tickets


st.set_page_config(
    page_title="IT 헬프데스크 자동화",
    page_icon="🎫",
    layout="wide",
)

st.title("🎫 IT 헬프데스크 자동 분류 시스템")
st.caption("AI 기반 티켓 분류 · 자동 응답 · BI 대시보드")

# ============ 사이드바 ============
with st.sidebar:
    st.header("⚙️ 시스템 상태")
    if os.getenv("ANTHROPIC_API_KEY"):
        st.success("✅ AI 분류 모드\n(Claude API 연동)")
    else:
        st.warning(
            "⚠️ 룰 기반 모드\n\n"
            "AI 모드를 사용하려면 `.env`에 `ANTHROPIC_API_KEY` 를 설정하세요."
        )

    st.divider()
    st.markdown("**관리 도구**")
    if st.button("🗑️ 전체 티켓 삭제", use_container_width=True):
        clear_tickets()
        st.success("모든 티켓이 삭제되었습니다.")
        st.rerun()

    st.divider()
    st.caption(
        "**About**\n\n"
        "Python + Streamlit + LLM API로 구축한 IT 헬프데스크 RPA 데모.\n"
        "AUMOVIO STAR IT Internship 포트폴리오용."
    )

# ============ 탭 ============
tab1, tab2, tab3 = st.tabs(["📝 문의 접수", "📊 대시보드", "📋 티켓 목록"])

# ----- 탭 1: 문의 접수 -----
with tab1:
    st.subheader("새 문의 접수")

    examples = {
        "(직접 입력)": "",
        "예시 1: VPN 연결 안됨": "VPN 연결이 안돼요. 재택근무 중인데 사내 시스템 접속 불가합니다.",
        "예시 2: 비밀번호 초기화": "비밀번호를 잊어버렸어요. 재설정 부탁드립니다.",
        "예시 3: 프린터 오류": "프린터에서 종이가 계속 걸려요.",
        "예시 4: 긴급 미팅 모니터": "회의실 모니터 출력이 안됩니다. 10분 뒤 미팅인데 급해요.",
    }
    pick = st.selectbox("예시 선택", list(examples.keys()))
    default_text = examples[pick]

    content = st.text_area(
        "문의 내용",
        value=default_text,
        height=120,
        placeholder="예: VPN이 안 됩니다...",
        key=f"content_{pick}",  # 예시 변경 시 텍스트 갱신
    )

    submit = st.button("🚀 분석 및 접수", type="primary")

    if submit and content.strip():
        with st.spinner("AI가 분석 중..."):
            result = classify_ticket(content)
            save_ticket(content, result)

        st.success("접수 완료!")

        c1, c2, c3 = st.columns(3)
        c1.metric("카테고리", result.get("category", "-"))

        priority = result.get("priority", "보통")
        priority_emoji = {"긴급": "🚨", "보통": "🟡", "낮음": "🟢"}.get(priority, "")
        c2.metric("우선순위", f"{priority_emoji} {priority}")

        c3.metric("담당자 배정", "필요" if result.get("needs_human") else "불필요")

        if result.get("summary"):
            st.info(f"**AI 요약**: {result['summary']}")

        if result.get("auto_reply"):
            st.markdown("### 💬 자동 응답 (1차)")
            st.markdown(result["auto_reply"])
        else:
            st.markdown("### 👤 담당자 배정 필요")
            st.markdown("자동 응답 가능 유형이 아니므로 담당자에게 라우팅됩니다.")

# ----- 탭 2: 대시보드 -----
with tab2:
    df = load_all_tickets()

    if df.empty:
        st.info(
            "아직 티켓이 없습니다.\n\n"
            "터미널에서 `python sample_data.py` 를 실행하면 샘플 데이터 20건이 자동 생성됩니다."
        )
    else:
        # KPI
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📨 전체 티켓", len(df))
        c2.metric("🚨 긴급", int((df["priority"] == "긴급").sum()))
        c3.metric("🤖 자동 응답", int((df["auto_reply"].fillna("") != "").sum()))
        c4.metric("👤 담당자 배정", int(df["needs_human"].sum()))

        st.divider()

        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader("카테고리별 분포")
            cat_counts = df["category"].value_counts().reset_index()
            cat_counts.columns = ["category", "count"]
            fig1 = px.pie(cat_counts, names="category", values="count", hole=0.4)
            fig1.update_layout(margin=dict(t=20, b=20, l=0, r=0))
            st.plotly_chart(fig1, use_container_width=True)

        with col_b:
            st.subheader("우선순위별 분포")
            priority_order = ["긴급", "보통", "낮음"]
            pri_counts = (
                df["priority"]
                .value_counts()
                .reindex(priority_order, fill_value=0)
                .reset_index()
            )
            pri_counts.columns = ["priority", "count"]
            color_map = {"긴급": "#EF4444", "보통": "#F59E0B", "낮음": "#10B981"}
            fig2 = px.bar(
                pri_counts,
                x="priority",
                y="count",
                color="priority",
                color_discrete_map=color_map,
                text="count",
            )
            fig2.update_layout(showlegend=False, margin=dict(t=20, b=20, l=0, r=0))
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("일자별 접수 추이")
        df["date"] = df["created_at"].dt.date
        daily = df.groupby("date").size().reset_index(name="count")
        fig3 = px.line(daily, x="date", y="count", markers=True)
        fig3.update_layout(margin=dict(t=20, b=20, l=0, r=0))
        st.plotly_chart(fig3, use_container_width=True)

# ----- 탭 3: 티켓 목록 -----
with tab3:
    df = load_all_tickets()
    if df.empty:
        st.info("티켓이 없습니다.")
    else:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            cat_options = df["category"].unique().tolist()
            cat_filter = st.multiselect(
                "카테고리 필터", options=cat_options, default=cat_options
            )
        with col_f2:
            pri_options = df["priority"].unique().tolist()
            pri_filter = st.multiselect(
                "우선순위 필터", options=pri_options, default=pri_options
            )

        filtered = df[
            df["category"].isin(cat_filter) & df["priority"].isin(pri_filter)
        ]

        st.dataframe(
            filtered[
                ["created_at", "category", "priority", "content", "summary", "needs_human"]
            ].rename(
                columns={
                    "created_at": "접수 시각",
                    "category": "카테고리",
                    "priority": "우선순위",
                    "content": "문의 내용",
                    "summary": "AI 요약",
                    "needs_human": "담당자 필요",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            label="📥 CSV로 내보내기",
            data=filtered.to_csv(index=False).encode("utf-8-sig"),
            file_name="tickets_export.csv",
            mime="text/csv",
        )
