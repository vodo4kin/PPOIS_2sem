import time
from unittest.mock import MagicMock, patch

import pytest

from atm.user_interface.display import Display
from atm.user_interface.keypad import Keypad
from atm.user_interface.session_timer import SessionTimer


class TestDisplay:
    def test_show_message_no_crash(self):
        d = Display()
        d.show_message("Hello")

    def test_ask_input(self):
        d = Display()
        with patch("builtins.input", return_value="  abc  "):
            assert d.ask_input("Prompt: ") == "abc"

    def test_show_menu(self):
        d = Display()
        with patch("builtins.input", return_value="1"):
            assert d.show_menu(["A", "B"]) == "1"


class TestKeypad:
    def test_read_input(self):
        k = Keypad()
        with patch("builtins.input", return_value="test"):
            assert k.read_input("> ") == "test"

    def test_read_pin(self):
        k = Keypad()
        with patch("builtins.input", return_value="1234"):
            assert k.read_pin() == "1234"


class TestSessionTimer:
    def test_reset(self):
        t = SessionTimer(timeout_seconds=1000)
        t.reset()
        assert t.last_activity <= time.time() + 1

    def test_check_timeout_no_timeout(self):
        t = SessionTimer(timeout_seconds=1000)
        assert t.check_timeout() is False

    def test_check_timeout_fires(self):
        callback = MagicMock()
        t = SessionTimer(timeout_seconds=0, callback=callback)
        time.sleep(0.01)
        assert t.check_timeout() is True
        callback.assert_called_once()
