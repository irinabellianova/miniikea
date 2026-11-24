import logging
import sys
from pathlib import Path

DEFAULT_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

def setup_logging(
        level: str = DEFAULT_LEVEL,
        log_file: str | None = None
):
    env_level = _env_to_log_level()
    if env_level:
        level = env_level

    numeric_level = getattr(logging, level.upper(), logging.INFO)

    root = logging.getLogger()
    root.setLevel(numeric_level)

    for handler in root.handlers[:]:
        root.removeHandler(handler)
        handler.close()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    root.addHandler(console_handler)

    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        root.addHandler(file_handler)

    return root

def _env_to_log_level() -> str | None:
    import os

    return os.environ.get("MINIIKEA_LOG_LEVEL")

setup_logging()