"""Offline fallback behavior of StackExchangeClient (README About + Notes).

Both tests run without network access: `requests` is patched to refuse (or is
absent, in which case the client's lazy import already fails), so the client
must exercise its bundled-sample fallback paths.
"""

import pytest

from stackoverflow_radar.client import StackExchangeClient
from stackoverflow_radar.config import Settings
from stackoverflow_radar.sample_data import load_sample_questions


@pytest.fixture()
def client() -> StackExchangeClient:
    return StackExchangeClient(settings=Settings())


def test_force_sample_returns_bundled_questions(client: StackExchangeClient) -> None:
    questions = client.fetch_questions(force_sample=True)
    sample_ids = {q.question_id for q in load_sample_questions()}

    assert questions
    assert all(q.source == "sample" for q in questions)
    assert {q.question_id for q in questions} <= sample_ids


def test_api_failure_falls_back_to_sample(
    client: StackExchangeClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    try:
        import requests
    except ImportError:
        requests = None  # absent dependency already forces the sample fallback

    if requests is not None:

        def refuse(*args: object, **kwargs: object) -> None:
            raise ConnectionError("offline test: no network")

        monkeypatch.setattr(requests, "get", refuse)

    questions = client.fetch_questions(use_sample_fallback=True)

    assert questions
    assert all(q.source == "sample" for q in questions)
