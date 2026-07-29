from flux.core.models import ColorPalette
from flux.core.enums import Theme
from flux.gui.themes.dark import DARK_THEME
from flux.gui.themes.light import LIGHT_THEME


class ThemeManager:
    def __init__(self) -> None:
        self._themes = {
            Theme.LIGHT: LIGHT_THEME,
            Theme.DARK: DARK_THEME,
        }
        self._current = DARK_THEME

    @property
    def colors(self) -> ColorPalette:
        return self._current.colors

    # TODO: Add proporties to access spacing and typography tokens

    def set_theme(self, theme: Theme) -> None:
        self._current = self._themes[theme]
