from src.utils.config import config


def test_config_contains_required_sections():
    assert config["project"]["name"]
    assert config["kafka"]["bootstrap_servers"]
    assert config["kafka"]["topics"]["raw"]
    assert config["replay"]["csv_path"]
    assert config["logging"]["level"] in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
