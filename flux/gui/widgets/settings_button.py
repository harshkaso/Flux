import dearpygui.dearpygui as dpg  # type: ignore
from typing import Callable, Optional
from flux.core.enums import ComponentTheme, Icon
from flux.core.types import ItemTag
from flux.theme.manager import ThemeManager


class SettingsButton:
    def __init__(self, icon: Icon, callback: Optional[Callable] = None) -> None:
        self._tag: ItemTag = dpg.generate_uuid()
        self._active: bool = False
        self._callback: Optional[Callable] = callback

        dpg.add_button(
            tag=self._tag, label=icon, width=40, height=40, callback=self._handle_click
        )

        ThemeManager.subscribe(self)

    def _handle_click(self) -> None:
        if self._callback:
            self._callback()

    @property
    def active(self) -> bool:
        return self._active

    def set_active(self, active: bool) -> None:
        self._active = active
        self.apply_theme()

    def apply_theme(self) -> None:
        dpg.bind_item_font(self._tag, font=ThemeManager.icon_font())
        component = (
            ComponentTheme.SETTINGS_BUTTON_ACTIVE
            if self._active
            else ComponentTheme.SETTINGS_BUTTON_NORMAL
        )

        dpg.bind_item_theme(self._tag, theme=ThemeManager.item_theme(component))
