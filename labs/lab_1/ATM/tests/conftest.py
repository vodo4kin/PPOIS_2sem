import tempfile
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def temp_data_dir(monkeypatch):
    tmp = Path(tempfile.mkdtemp())
    import atm.config as config_module
    monkeypatch.setattr(config_module.Config, "DATA_DIR", tmp)
    monkeypatch.setattr(
        config_module.Config, "ATM_STATE_FILE", tmp / "atm_state.json"
    )
    monkeypatch.setattr(
        config_module.Config, "BANK_ACCOUNTS_FILE", tmp / "bank_accounts.json"
    )
    config_module.Config.ensure_data_dir()
    yield tmp
