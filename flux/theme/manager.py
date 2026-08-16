from pathlib import Path
from typing import Callable
import dearpygui.dearpygui as dpg  # type: ignore

from flux.core.types import ItemTag
from flux.core.protocols import ThemeSubscriber
from flux.core.enums import Theme, ComponentTheme
from flux.theme.models import ThemeSpec

from flux.theme.builders.sidebar import build_sidebar_theme
from flux.theme.builders.inspector import build_inspector_theme
from flux.theme.builders.settings_rail import build_settings_rail_theme
from flux.theme.builders.app_window import build_app_window_theme
from flux.theme.builders.application import build_application_theme
from flux.theme.builders.collapsible_panel import (
    build_collapsible_panel_theme,
    build_collapsible_panel_header_theme,
    build_collapsible_panel_body_theme,
)
from flux.theme.builders.settings_button import (
    build_settings_button_normal_theme,
    build_settings_button_active_theme,
)

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
        ComponentTheme.INSPECTOR: build_inspector_theme,
        ComponentTheme.SETTINGS_RAIL: build_settings_rail_theme,
        ComponentTheme.SETTINGS_BUTTON_NORMAL: build_settings_button_normal_theme,
        ComponentTheme.SETTINGS_BUTTON_ACTIVE: build_settings_button_active_theme,
        ComponentTheme.COLLAPSIBLE_PANEL: build_collapsible_panel_theme,
        ComponentTheme.COLLAPSIBLE_PANEL_HEADER: build_collapsible_panel_header_theme,
        ComponentTheme.COLLAPSIBLE_PANEL_BODY: build_collapsible_panel_body_theme,
    }
    _subscribers: list[ThemeSubscriber] = []
    _compiled: dict[ComponentTheme, ItemTag] = {}
    _initialized: bool = False
    _regular_font: ItemTag
    _icon_font: ItemTag

    @classmethod
    def _build_component_themes(cls):
        cls._compiled.clear()
        for component, builder in cls._builders.items():
            cls._compiled[component] = builder(cls._current)

    @classmethod
    def _register_fonts(cls) -> None:
        path = Path(__file__).parent / "fonts"
        with dpg.font_registry():
            cls._regular_font = dpg.add_font(
                file=str(path / cls._current.regular_font.filename),
                size=cls._current.regular_font.size,
            )
            cls._icon_font = dpg.add_font(
                file=str(path / cls._current.icon_font.filename),
                size=cls._current.icon_font.size,
            )

    @classmethod
    def _ensure_initialized(cls):
        if not cls._initialized:
            cls._register_fonts()
            cls._build_component_themes()
            cls._initialized = True

    @classmethod
    def item_theme(cls, componentTheme: ComponentTheme) -> ItemTag:
        cls._ensure_initialized()
        return cls._compiled[componentTheme]

    @classmethod
    def regular_font(cls) -> ItemTag:
        cls._ensure_initialized()
        return cls._regular_font

    @classmethod
    def icon_font(cls) -> ItemTag:
        cls._ensure_initialized()
        return cls._icon_font

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
