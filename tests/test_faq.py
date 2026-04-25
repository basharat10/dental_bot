from core.faq import get_faq_answer


def test_faq_hours_match():
    answer = get_faq_answer("What are your opening hours?")
    assert answer is not None
    assert "open" in answer.lower()


def test_faq_no_match_returns_none():
    assert get_faq_answer("I would like to discuss billing details.") is None
