from pathlib import Path
import yaml


class Config:
    """
    Loads application configuration from settings.yaml.
    The configuration is loaded only once and reused.
    """

    _config = None

    @classmethod
    def load(cls):
        if cls._config is None:

            project_root = Path(__file__).resolve().parents[2]
            config_path = project_root / "configs" / "settings.yaml"

            if not config_path.exists():
                raise FileNotFoundError(
                    f"Configuration file not found: {config_path}"
                )

            with open(config_path, "r", encoding="utf-8") as file:
                cls._config = yaml.safe_load(file)

            if cls._config is None:
                raise ValueError("settings.yaml is empty or invalid.")

        return cls._config


config = Config.load()