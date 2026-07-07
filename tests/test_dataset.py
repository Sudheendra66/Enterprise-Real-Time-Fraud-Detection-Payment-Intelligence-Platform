from pathlib import Path

from src.utils.config import config


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_replay_dataset_path_is_configured():
    dataset_path = PROJECT_ROOT / config["replay"]["csv_path"]

    assert dataset_path.suffix == ".csv"
    assert dataset_path.parent.name == "raw"
