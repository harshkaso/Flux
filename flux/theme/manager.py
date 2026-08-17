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
from flux.utils.logger import get_logger

logger = get_logger(__file__)


class ThemeManager:
    _FONTS_DIR: Path = Path(__file__).parent / "fonts"
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
    _fonts: dict[tuple[str, int], ItemTag] = {}
    _font_registry: ItemTag
    _regular_font: ItemTag
    _icon_font: ItemTag

    @classmethod
    def _build_component_themes(cls):
        if cls._compiled:
            logger.warning("component themes already built.")
            return
        for component, builder in cls._builders.items():
            cls._compiled[component] = builder(cls._current)

    @classmethod
    def _add_regular_font(cls, filename: str, size: int, registry: ItemTag) -> None:
        cls._regular_font = dpg.add_font(
            str(cls._FONTS_DIR / filename),
            size,
            parent=registry,
        )
        cls._fonts[(filename, size)] = cls._regular_font

    @classmethod
    def _add_icon_font(cls, filename: str, size: int, registry: ItemTag) -> None:
        cls._icon_font = dpg.add_font(
            str(cls._FONTS_DIR / filename),
            size,
            parent=registry,
        )
        cls._fonts[(filename, size)] = cls._icon_font

    @classmethod
    def _get_or_add_font(
        cls,
        filename: str,
        size: int,
    ) -> ItemTag:
        key = (filename, size)

        if key not in cls._fonts:
            cls._fonts[key] = dpg.add_font(
                str(cls._FONTS_DIR / filename),
                size,
                parent=cls._font_registry,
            )

        return cls._fonts[key]

    @classmethod
    def _register_fonts(cls) -> None:
        cls._font_registry = dpg.add_font_registry()
        cls._regular_font = cls._get_or_add_font(
            cls._current.regular_font.filename,
            cls._current.regular_font.size,
        )
        cls._icon_font = cls._get_or_add_font(
            cls._current.icon_font.filename,
            cls._current.icon_font.size,
        )

    @classmethod
    def _delete_compiled(cls):
        if cls._compiled:
            for compiled_theme in cls._compiled.values():
                dpg.delete_item(compiled_theme)
            cls._compiled.clear()

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
        cls._regular_font = cls._get_or_add_font(
            cls._current.regular_font.filename,
            cls._current.regular_font.size,
        )
        cls._icon_font = cls._get_or_add_font(
            cls._current.icon_font.filename,
            cls._current.icon_font.size,
        )
        # Delete existing compiled themes before building new ones
        cls._delete_compiled()
        cls._build_component_themes()
        for subscriber in cls._subscribers:
            subscriber.apply_theme()
