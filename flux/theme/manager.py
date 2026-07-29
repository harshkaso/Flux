from flux.core.types import ItemTag
from flux.core.protocols import Themeable
from flux.core.enums import Theme, ComponentTheme
from flux.core.models import ThemeSpec, ColorPalette

from flux.theme.dark import DARK_THEME
from flux.theme.light import LIGHT_THEME

from flux.theme.builders.app_window import AppWindowTheme


class ThemeManager:
    def __init__(self) -> None:
        self._themes: dict[Theme, ThemeSpec] = {
            Theme.LIGHT: LIGHT_THEME,
            Theme.DARK: DARK_THEME,
        }
        self._subscribers: list[Themeable] = []
        self._compiled: dict[ComponentTheme, ItemTag] = {}
        self._current: ThemeSpec = DARK_THEME

        self._rebuild()

    @property
    def colors(self) -> ColorPalette:
        return self._current.colors

    # TODO: Add proporties to access spacing and typography tokens

    def _rebuild(self) -> None:
        self._compiled[ComponentTheme.APP_WINDOW] = AppWindowTheme().build(
            self._current
        )

    def item_theme(self, component: ComponentTheme) -> ItemTag:
        return self._compiled[component]

    def subscribe(self, subscriber: Themeable) -> None:
        self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber: Themeable) -> None:
        self._subscribers.remove(subscriber)

    def set_theme(self, theme: Theme) -> None:
        self._current = self._themes[theme]
        self._rebuild()
        for subscriber in self._subscribers:
            subscriber.apply_theme()
