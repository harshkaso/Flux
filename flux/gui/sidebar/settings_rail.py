from typing import Callable

import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.enums import ComponentTheme, Icon
from flux.core.types import ItemTag
from flux.core.enums import SettingsPage
from flux.gui.widgets.settings_button import SettingsButton
from flux.theme.manager import ThemeManager


class SettingsRail:
    def __init__(
        self, on_settings_button_selected: Callable[[SettingsPage], None]
    ) -> None:
        self._tag: ItemTag = dpg.generate_uuid()
        self._on_settings_button_selected = on_settings_button_selected
        self._active_settings_button: SettingsButton | None = None
        with dpg.child_window(tag=self._tag, width=56):
            self._buttons: dict[SettingsPage, SettingsButton] = {
                SettingsPage.FLOWFIELD: SettingsButton(
                    icon=Icon.WIND,
                    callback=lambda: self.select(SettingsPage.FLOWFIELD),
                ),
                SettingsPage.PARTICLE: SettingsButton(
                    icon=Icon.BUBBLES,
                    callback=lambda: self.select(SettingsPage.PARTICLE),
                ),
                SettingsPage.MASK: SettingsButton(
                    icon=Icon.SQUARE_INTERSECT,
                    callback=lambda: self.select(SettingsPage.MASK),
                ),
                SettingsPage.COLOR: SettingsButton(
                    icon=Icon.PAINTBRUSH_VERTICAL,
                    callback=lambda: self.select(SettingsPage.COLOR),
                ),
                SettingsPage.SAVE: SettingsButton(
                    icon=Icon.SAVE,
                    callback=lambda: self.select(SettingsPage.SAVE),
                ),
                SettingsPage.GENERAL: SettingsButton(
                    icon=Icon.COG,
                    callback=lambda: self.select(SettingsPage.GENERAL),
                ),
            }
        ThemeManager.subscribe(self)

    def set_active_button(self, tool_button: SettingsButton) -> None:
        if self._active_settings_button:
            self._active_settings_button.set_active(False)
        tool_button.set_active(True)
        self._active_settings_button = tool_button

    def select(self, page: SettingsPage) -> None:
        self.set_active_button(self._buttons[page])
        self._on_settings_button_selected(page)

    def apply_theme(self) -> None:
        dpg.bind_item_theme(
            self._tag,
            ThemeManager.item_theme(componentTheme=ComponentTheme.SETTINGS_RAIL),
        )
