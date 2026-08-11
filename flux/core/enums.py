from enum import StrEnum, auto


class LogLevel(StrEnum):
    @staticmethod
    def _generate_next_value_(
        name: str,
        start: int,
        count: int,
        last_values: list[str],
    ) -> str:
        return name.upper()

    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class Theme(StrEnum):
    LIGHT = auto()
    DARK = auto()


class ComponentTheme(StrEnum):
    APPLICATION = auto()
    APP_WINDOW = auto()
    SIDEBAR = auto()
    SETTINGS_RAIL = auto()
    INSPECTOR = auto()
    CANVAS = auto()
    LOADING = auto()
    BUTTON = auto()
    TOOL_BUTTON_NORMAL = auto()
    TOOL_BUTTON_ACTIVE = auto()


class SettingsPage(StrEnum):
    FLOWFIELD = auto()
    PARTICLE = auto()
    MASK = auto()
    COLOR = auto()
    SAVE = auto()


class IconID(StrEnum):
    @staticmethod
    def _generate_next_value_(
        name: str,
        start: int,
        count: int,
        last_values: list[str],
    ) -> str:
        return name.lower().replace("_", "-")

    CHEVRON_RIGHT = auto()
    CHEVRON_DOWN = auto()
    WAVES_HORIZONTAL = auto()
    SPARKLES = auto()
    PALETTE = auto()
    DOWNLOAD = auto()
    SCAN = auto()
    SAVE = auto()
