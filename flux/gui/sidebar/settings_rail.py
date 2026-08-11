from typing import Callable

import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.enums import ComponentTheme, IconID
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
                    icon=IconID.WAVES_HORIZONTAL,
                    callback=lambda: self._select(SettingsPage.FLOWFIELD),
                ),
                SettingsPage.PARTICLE: SettingsButton(
                    icon=IconID.SPARKLES,
                    callback=lambda: self._select(SettingsPage.PARTICLE),
                ),
                SettingsPage.MASK: SettingsButton(
                    icon=IconID.SCAN,
                    callback=lambda: self._select(SettingsPage.MASK),
                ),
                SettingsPage.COLOR: SettingsButton(
                    icon=IconID.PALETTE,
                    callback=lambda: self._select(SettingsPage.COLOR),
                ),
                SettingsPage.SAVE: SettingsButton(
                    icon=IconID.SAVE,
                    callback=lambda: self._select(SettingsPage.SAVE),
                ),
            }
        ThemeManager.subscribe(self)
        self.set_active_button(self._buttons[SettingsPage.FLOWFIELD])

    def set_active_button(self, tool_button: SettingsButton) -> None:
        if self._active_settings_button:
            self._active_settings_button.set_active(False)
        tool_button.set_active(True)
        self._active_settings_button = tool_button

    def _select(self, page: SettingsPage) -> None:
        self.set_active_button(self._buttons[page])
        self._on_settings_button_selected(page)

    def apply_theme(self) -> None:
        dpg.bind_item_theme(
            self._tag,
            ThemeManager.item_theme(componentTheme=ComponentTheme.SETTINGS_RAIL),
        )
