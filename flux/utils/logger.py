import json
import logging
import logging.config
from enum import Enum
from pathlib import Path
from datetime import datetime
from typing import Type


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
    config: Type[LoggerConfig] = LoggerConfig,
    name: str | None = None,
) -> logging.Logger:
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        with open(config.config_file, "r", encoding="utf-8") as f:
            config_text = f.read()
        config_text.replace("%(date)s", today)
        dict_config = json.loads(config_text)
        if config.level and "root" in dict_config:
            dict_config["root"]["level"] = config.level.value
        Path("logs").mkdir(exist_ok=True)
        logging.config.dictConfig(dict_config)

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
