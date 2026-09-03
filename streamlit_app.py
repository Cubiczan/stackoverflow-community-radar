from __future__ import annotations

import streamlit as st

from stackoverflow_radar.client import StackExchangeClient
from stackoverflow_radar.graph import build_topic_graph, cluster_questions, summarize_graph
from stackoverflow_radar.insights import build_answer_brief, priority_score, rank_questions


st.set_page_config(page_title="Stack Overflow Community Radar", layout="wide")


def main() -> None:
    st.title("Stack Overflow Community Radar")
    st.caption("Rank unanswered questions, see tag clusters, and draft answer briefs.")

    with st.sidebar:
        st.header("Data Source")
        source = st.radio("Mode", ["Sample data", "Live Stack Exchange"], index=0)
        tags_text = st.text_input("Tags", value="python,sqlalchemy")
        query = st.text_input("Search", value="")
        page_size = st.slider("Questions", min_value=5, max_value=100, value=30, step=5)
        refresh = st.button("Refresh")

    if refresh:
        st.rerun()

    client = StackExchangeClient()
    tags = [tag.strip() for tag in tags_text.split(",") if tag.strip()]
    use_sample = source == "Sample data"

    questions = client.fetch_questions(
        tags=tags or None,
        query=query or None,
        page_size=page_size,
        force_sample=use_sample,
        use_sample_fallback=True,
    )

    ranked = rank_questions(questions)
    graph = build_topic_graph(ranked)
    clusters = cluster_questions(ranked)
    summary = summarize_graph(graph)

    total = len(ranked)
    unanswered = sum(1 for question in ranked if not question.is_answered)
    avg_priority = round(sum(priority_score(question) for question in ranked) / total, 2) if ranked else 0.0
    avg_score = round(sum(question.score for question in ranked) / total, 2) if ranked else 0.0

    metric_cols = st.columns(4)
    metric_cols[0].metric("Questions", total)
    metric_cols[1].metric("Unanswered", unanswered)
    metric_cols[2].metric("Avg score", avg_score)
    metric_cols[3].metric("Avg priority", avg_priority)

    left, right = st.columns([1.3, 1])

    with left:
        st.subheader("Priority queue")
        for question in ranked[:10]:
            with st.container(border=True):
                st.markdown(f"**{question.title}**")
                st.write(
                    f"Tags: {', '.join(question.tags) or 'none'} | Score: {question.score} | Answers: {question.answer_count} | Views: {question.view_count} | Priority: {priority_score(question)}"
                )
                st.write(question.body[:240] + ("..." if len(question.body) > 240 else ""))
                st.write(question.link)

    with right:
        st.subheader("Graph summary")
        st.json(summary)
        st.subheader("Topic clusters")
        for cluster in clusters[:6]:
            with st.expander(f"{cluster.name} ({len(cluster.question_ids)} questions)"):
                st.write(f"Unanswered: {cluster.unanswered_count}")
                st.write(f"Avg score: {cluster.average_score}")
                st.write(f"Avg priority: {cluster.average_priority}")
                st.write(f"Tags: {', '.join(cluster.tags) or 'none'}")

    st.subheader("Answer brief")
    selected_titles = [question.title for question in ranked]
    if selected_titles:
        selected_title = st.selectbox("Choose a question", selected_titles)
        selected_question = next(question for question in ranked if question.title == selected_title)
        related = [question for question in ranked if question.question_id != selected_question.question_id and set(question.tags).intersection(selected_question.tags)]
        brief = build_answer_brief(selected_question, related_questions=related)
        st.json(brief.to_dict())


if __name__ == "__main__":
    main()
