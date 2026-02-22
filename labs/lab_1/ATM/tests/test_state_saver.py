import pytest

from atm.session_manager.state_saver import StateSaver


class TestStateSaver:
    def test_save_and_load(self, temp_data_dir):
        saver = StateSaver()
        state = {"key": "value", "n": 42}
        saver.save(state)
        loaded = saver.load()
        assert loaded["key"] == "value"
        assert loaded["n"] == 42

    def test_load_missing_returns_empty(self, temp_data_dir):
        saver = StateSaver()
        loaded = saver.load()
        assert loaded == {}
