from core.session import is_session_expired


def test_session_not_expired_within_timeout():
    assert is_session_expired(last_activity_at=100.0, now=120.0, timeout_seconds=30) is False


def test_session_expired_after_timeout():
    assert is_session_expired(last_activity_at=100.0, now=140.1, timeout_seconds=30) is True
