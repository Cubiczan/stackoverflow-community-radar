from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from .insights import priority_score
from .models import ClusterSummary, Question


@dataclass(slots=True)
class TopicGraph:
    nodes: dict[str, dict[str, object]] = field(default_factory=dict)
    edges: dict[tuple[str, str], int] = field(default_factory=dict)

    def add_node(self, node_id: str, **attrs: object) -> None:
        self.nodes[node_id] = {**self.nodes.get(node_id, {}), **attrs}

    def add_edge(self, left: str, right: str, weight: int = 1) -> None:
        key = tuple(sorted((left, right)))
        self.edges[key] = self.edges.get(key, 0) + weight

    def number_of_nodes(self) -> int:
        return len(self.nodes)

    def number_of_edges(self) -> int:
        return len(self.edges)

    def degree(self, node_id: str) -> int:
        return sum(weight for (left, right), weight in self.edges.items() if left == node_id or right == node_id)


def build_topic_graph(questions: list[Question]) -> TopicGraph:
    graph = TopicGraph()
    for question in questions:
        q_node = f"q:{question.question_id}"
        graph.add_node(
            q_node,
            kind="question",
            title=question.title,
            score=question.score,
            answered=question.is_answered,
            priority=priority_score(question),
            tags=question.tags,
        )
        for tag in question.tags:
            t_node = f"tag:{tag}"
            graph.add_node(t_node, kind="tag", tag=tag)
            graph.add_edge(q_node, t_node, weight=1)

    tag_weights: dict[tuple[str, str], int] = defaultdict(int)
    for question in questions:
        tags = list(dict.fromkeys(question.tags))
        for idx, left in enumerate(tags):
            for right in tags[idx + 1 :]:
                tag_weights[tuple(sorted((left, right)))] += 1
    for (left, right), weight in tag_weights.items():
        graph.add_edge(f"tag:{left}", f"tag:{right}", weight=weight)
    return graph


def cluster_questions(questions: list[Question]) -> list[ClusterSummary]:
    buckets: dict[str, list[Question]] = defaultdict(list)
    for question in questions:
        key = question.tags[0] if question.tags else "untagged"
        buckets[key].append(question)

    clusters: list[ClusterSummary] = []
    for name, items in sorted(buckets.items(), key=lambda item: (-len(item[1]), item[0])):
        tags = sorted({tag for q in items for tag in q.tags})
        unanswered = sum(1 for q in items if not q.is_answered)
        clusters.append(
            ClusterSummary(
                name=name,
                tags=tags[:6],
                question_ids=[q.question_id for q in items],
                unanswered_count=unanswered,
                average_score=round(sum(q.score for q in items) / len(items), 2),
                average_priority=round(sum(priority_score(q) for q in items) / len(items), 2),
            )
        )
    return clusters


def summarize_graph(graph: TopicGraph) -> dict[str, object]:
    question_nodes = [node for node, data in graph.nodes.items() if data.get("kind") == "question"]
    tag_nodes = [node for node, data in graph.nodes.items() if data.get("kind") == "tag"]
    top_tags = sorted(
        (
            (node.replace("tag:", ""), graph.degree(node))
            for node in tag_nodes
        ),
        key=lambda item: (-item[1], item[0]),
    )[:5]
    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "questions": len(question_nodes),
        "tags": len(tag_nodes),
        "top_tags": [{"tag": tag, "connections": degree} for tag, degree in top_tags],
    }
