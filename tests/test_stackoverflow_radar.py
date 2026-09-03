from stackoverflow_radar.graph import build_topic_graph, cluster_questions, summarize_graph
from stackoverflow_radar.insights import build_answer_brief, priority_score, rank_questions
from stackoverflow_radar.sample_data import load_sample_questions


def test_rank_questions_prioritizes_unanswered_threads() -> None:
    questions = load_sample_questions()
    ranked = rank_questions(questions)

    assert ranked[0].is_answered is False
    assert priority_score(ranked[0]) >= priority_score(ranked[-1])


def test_topic_graph_builds_tag_network() -> None:
    questions = load_sample_questions()
    graph = build_topic_graph(questions)
    summary = summarize_graph(graph)

    assert summary["questions"] == len(questions)
    assert summary["tags"] > 0
    assert summary["edges"] > summary["questions"]


def test_cluster_and_brief_shapes() -> None:
    questions = load_sample_questions()
    clusters = cluster_questions(questions)
    brief = build_answer_brief(questions[0], related_questions=questions[1:3])

    assert clusters
    assert brief.outline
    assert brief.question_id == questions[0].question_id
