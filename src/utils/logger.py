import json
import logging
import logging.config
from enum import Enum
from pathlib import Path
from datetime import datetime


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggerConfig:
    level: LogLevel = LogLevel.INFO
    config_file: str = f"{Path(__file__).parent}/logging.json"


def setup_logger(
    level: LogLevel = LoggerConfig.level,
    config_file: str = LoggerConfig.config_file,
    name: str | None = None,
) -> logging.Logger:
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        with open(config_file, "r", encoding="utf-8") as f:
            config_text = f.read()
        config_text.replace("%(date)s", today)
        config = json.loads(config_text)
        if level and "root" in config:
            config["root"]["level"] = level.value
        Path("logs").mkdir(exist_ok=True)
        logging.config.dictConfig(config)

        logger = get_logger(name)

        logger.info(f"\nLog files created with date: {today}\n{'.'*100}")
        return logger

    except Exception as e:
        logging.basicConfig(level=logging.INFO)
        logger = get_logger(name)
        logger.error(f"Failed to load logging configuration: {e}")
        return logger


def get_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name)


def shutdown_loggers() -> None:
    logging.shutdown()
