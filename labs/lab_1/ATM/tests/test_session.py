import pytest

from atm.session_manager.session import Session
from atm.session_manager.session_type import SessionType


class TestSession:
    def test_start_and_end(self):
        s = Session()
        assert s.is_active is False
        s.start(SessionType.CLIENT, "1234")
        assert s.is_active is True
        assert s.user_id == "1234"
        s.end()
        assert s.is_active is False

    def test_double_start_raises(self):
        s = Session()
        s.start(SessionType.CLIENT, "1")
        with pytest.raises(RuntimeError, match="already active"):
            s.start(SessionType.CLIENT, "2")

    def test_end_without_start_no_op(self):
        """Calling end() when no active session is a no-op (idempotent)."""
        s = Session()
        s.end()
        assert s.is_active is False
