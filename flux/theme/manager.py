from typing import Callable

from flux.core.types import ItemTag
from flux.core.protocols import ThemeSubscriber
from flux.core.enums import Theme, ComponentTheme
from flux.theme.models import ThemeSpec, ColorPalette
from flux.theme.builders.button import build_button_theme
from flux.theme.builders.sidebar import build_sidebar_theme
from flux.theme.builders.application import build_application_theme
from flux.theme.builders.app_window import build_app_window_theme

from flux.theme.dark import DARK_THEME
from flux.theme.light import LIGHT_THEME


class ThemeManager:
    _themes: dict[Theme, ThemeSpec] = {
        Theme.LIGHT: LIGHT_THEME,
        Theme.DARK: DARK_THEME,
    }
    _current: ThemeSpec = DARK_THEME
    _builders: dict[ComponentTheme, Callable[[ThemeSpec], ItemTag]] = {
        ComponentTheme.APPLICATION: build_application_theme,
        ComponentTheme.APP_WINDOW: build_app_window_theme,
        ComponentTheme.SIDEBAR: build_sidebar_theme,
        ComponentTheme.BUTTON: build_button_theme,
    }
    _subscribers: list[ThemeSubscriber] = []
    _compiled: dict[ComponentTheme, ItemTag] = {}

    @property
    def colors(cls) -> ColorPalette:
        return cls._current.colors

    @classmethod
    def _ensure_initialized(cls):
        if not cls._compiled:
            cls._build_component_themes()

    @classmethod
    def _build_component_themes(cls):
        cls._compiled.clear()
        for component, builder in cls._builders.items():
            cls._compiled[component] = builder(cls._current)

    @classmethod
    def item_theme(cls, componentTheme: ComponentTheme) -> ItemTag:
        cls._ensure_initialized()
        return cls._compiled[componentTheme]

    @classmethod
    def subscribe(cls, subscriber: ThemeSubscriber) -> None:
        cls._subscribers.append(subscriber)
        subscriber.apply_theme()

    @classmethod
    def set_theme(cls, theme: Theme) -> None:
        cls._current = cls._themes[theme]
        cls._build_component_themes()
        for subscriber in cls._subscribers:
            subscriber.apply_theme()
