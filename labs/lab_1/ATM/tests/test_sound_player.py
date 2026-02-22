from unittest.mock import MagicMock

import pytest

from atm.user_interface.sound_player import SoundPlayer


class TestSoundPlayer:
    def test_beep_success(self):
        log = MagicMock()
        sp = SoundPlayer(log)
        sp.beep_success()
        log.info.assert_called_once_with("*Beep*")

    def test_beep_error(self):
        log = MagicMock()
        sp = SoundPlayer(log)
        sp.beep_error()
        log.error.assert_called_once_with("*Beep*")
