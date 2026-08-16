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
    BUTTON = auto()
    SETTINGS_BUTTON_NORMAL = auto()
    SETTINGS_BUTTON_ACTIVE = auto()
    COLLAPSIBLE_PANEL = auto()
    COLLAPSIBLE_PANEL_HEADER = auto()
    COLLAPSIBLE_PANEL_BODY = auto()


class SettingsPage(StrEnum):
    FLOWFIELD = auto()
    PARTICLE = auto()
    MASK = auto()
    COLOR = auto()
    SAVE = auto()
    GENERAL = auto()


class Icon(StrEnum):
    BUBBLES = "\U000f0000"
    CHEVRON_DOWN = "\U000f0001"
    CHEVRON_RIGHT = "\U000f0002"
    COG = "\U000f0003"
    PAINTBRUSH_VERTICAL = "\U000f0004"
    SAVE = "\U000f0005"
    SQUARE_INTERSECT = "\U000f0006"
    WIND = "\U000f0007"
