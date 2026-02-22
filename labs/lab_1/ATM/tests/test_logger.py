import tempfile
from pathlib import Path

from atm.session_manager.logger import Logger


class TestLogger:
    def test_info_warning_error(self):
        with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
            path = f.name
        try:
            log = Logger(log_file=path)
            log.info("info msg")
            log.warning("warn msg")
            log.error("err msg")
            log.close()
            content = Path(path).read_text()
            assert "info msg" in content
            assert "warn msg" in content
            assert "err msg" in content
        finally:
            Path(path).unlink(missing_ok=True)

    def test_no_file(self):
        log = Logger(log_file=None)
        log.info("x")
