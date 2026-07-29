from enum import Enum, auto


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Theme(str, Enum):
    LIGHT = "light"
    DARK = "dark"


class ComponentTheme(Enum):
    APPLICATION = auto()
    APP_WINDOW = auto()
    SIDEBAR = auto()
    TOOL_RAIL = auto()
    INSPECTOR = auto()
    CANVAS = auto()
    LOADING = auto()
