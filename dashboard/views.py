import streamlit as st
import pandas as pd
import altair as alt
from memory.journal_db import get_entries
from agents.insight_agent import detect_patterns


def show_dashboard():

    try:
        docs, metadatas = get_entries()

        if not docs:
            st.info("No journal entries yet. Start chatting to build your history.")
            return

        # ── Emotion pattern chart ──────────────────────────────────────────
        st.subheader("🧠 Emotion Patterns")

        patterns = detect_patterns()
        emotion_labels = ["stress", "sadness", "anger", "happiness"]

        chart_df = pd.DataFrame({
            "Emotion": [e.capitalize() for e in emotion_labels],
            "Count":   [patterns[e] for e in emotion_labels],
        })

        color_scale = alt.Scale(
            domain=["Stress", "Sadness", "Anger", "Happiness"],
            range=["#e05c5c", "#7b9cdb", "#e0955c", "#5cba7d"],
        )

        bar_chart = (
            alt.Chart(chart_df)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("Emotion:N", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Count:Q", axis=alt.Axis(tickMinStep=1)),
                color=alt.Color("Emotion:N", scale=color_scale, legend=None),
                tooltip=["Emotion", "Count"],
            )
            .properties(height=280)
        )

        st.altair_chart(bar_chart, use_container_width=True)

        # ── Summary metrics ────────────────────────────────────────────────
        st.subheader("📊 Summary")

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Entries",  patterns["total_entries"])
        col2.metric("😰 Stress",      patterns["stress"])
        col3.metric("😢 Sadness",     patterns["sadness"])
        col4.metric("😠 Anger",       patterns["anger"])
        col5.metric("😊 Happiness",   patterns["happiness"])

        # ── Timeline ───────────────────────────────────────────────────────
        st.subheader("📅 Journal Timeline")

        for doc, meta in zip(reversed(docs), reversed(metadatas)):
            date = meta.get("date", "Unknown date")
            with st.expander(f"🗓 {date}"):
                st.write(doc)

    except Exception as e:
        st.error(f"Dashboard error: {e}")