from importlib.resources import files
from pathlib import Path
import yaml
from typing import Any, Dict, Optional


def load_default_config() -> Dict[str, Any]:
    data = files("vibe_sweeper.config").joinpath("default_rules.yaml").read_text(encoding="utf-8")
    return yaml.safe_load(data)


def load_config_from_path(path: Optional[Path]) -> Dict[str, Any]:
    cfg = load_default_config()
    if path and path.is_file():
        user_data = path.read_text(encoding="utf-8")
        user_cfg = yaml.safe_load(user_data) or {}
        cfg.update(user_cfg)
    return cfg
