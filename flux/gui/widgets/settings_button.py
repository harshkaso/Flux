import dearpygui.dearpygui as dpg  # type: ignore
from typing import Callable
from flux.core.enums import ComponentTheme, IconID
from flux.core.types import ItemTag
from flux.gui.widgets.icon import IconWidget
from flux.theme.manager import ThemeManager


class SettingsButton:
    def __init__(
        self, icon: IconID, callback: Callable[[], None] | None = None
    ) -> None:
        self._tag: ItemTag = dpg.generate_uuid()
        self._clickable_tag: ItemTag = dpg.generate_uuid()
        self._handler_registry: ItemTag = dpg.generate_uuid()
        self._active: bool = False
        self._callback = callback

        # with dpg.child_window(tag=self._tag, width=40, height=40):
        with dpg.child_window(tag=self._tag, auto_resize_y=True, auto_resize_x=True):
            with dpg.group(tag=self._clickable_tag):
                self._icon = IconWidget(icon=icon)

        with dpg.item_handler_registry(tag=self._handler_registry):
            dpg.add_item_clicked_handler(
                callback=self._handle_click,
            )

        dpg.bind_item_handler_registry(
            self._clickable_tag,
            self._handler_registry,
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
        component = (
            ComponentTheme.TOOL_BUTTON_ACTIVE
            if self._active
            else ComponentTheme.TOOL_BUTTON_NORMAL
        )

        dpg.bind_item_theme(self._tag, theme=ThemeManager.item_theme(component))
