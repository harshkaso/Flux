from flux.core.types import ItemTag
from flux.core.protocols import Themeable
from flux.core.enums import Theme, ComponentTheme
from flux.core.models import ThemeSpec, ColorPalette

from flux.theme.dark import DARK_THEME
from flux.theme.light import LIGHT_THEME

from flux.theme.builders.application import build_application_theme
from flux.theme.builders.app_window import build_app_window_theme


class ThemeManager:
    def __init__(self) -> None:
        self._themes: dict[Theme, ThemeSpec] = {
            Theme.LIGHT: LIGHT_THEME,
            Theme.DARK: DARK_THEME,
        }
        self._subscribers: list[Themeable] = []
        self._compiled: dict[ComponentTheme, ItemTag] = {}
        self._current: ThemeSpec = DARK_THEME

        self._build_themes()

    @property
    def colors(self) -> ColorPalette:
        return self._current.colors

    # TODO: Add proporties to access spacing and typography tokens

    def _build_themes(self) -> None:
        self._compiled[ComponentTheme.APPLICATION] = build_application_theme(
            self._current
        )
        self._compiled[ComponentTheme.APP_WINDOW] = build_app_window_theme(
            self._current
        )

    def item_theme(self, componentTheme: ComponentTheme) -> ItemTag:
        return self._compiled[componentTheme]

    def subscribe(self, subscriber: Themeable) -> None:
        self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber: Themeable) -> None:
        self._subscribers.remove(subscriber)

    def set_theme(self, theme: Theme) -> None:
        self._current = self._themes[theme]
        self._build_themes()
        for subscriber in self._subscribers:
            subscriber.apply_theme()
