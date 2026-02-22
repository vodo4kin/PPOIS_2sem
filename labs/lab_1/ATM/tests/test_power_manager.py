from atm.power_hardware.power_manager import PowerManager


class TestPowerManager:
    def test_shutdown_startup(self):
        pm = PowerManager()
        pm.shutdown()
        assert pm.is_powered is False
        pm.startup()
        assert pm.is_powered is True
