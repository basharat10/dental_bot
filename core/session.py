def is_session_expired(last_activity_at, now, timeout_seconds):
    if timeout_seconds <= 0:
        return True
    return (now - last_activity_at) > timeout_seconds
