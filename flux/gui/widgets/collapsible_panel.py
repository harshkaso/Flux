# All hail the G.O.A.T Vladimir Ein for figuring out the way to get rid of deadzones on the header button of this widget
from typing import Optional

import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.enums import ComponentTheme, Icon
from flux.core.types import ItemTag

from flux.theme.manager import ThemeManager


class CollapsiblePanel:
    def __init__(
        self,
        label: str,
        default_open: Optional[bool] = True,
    ) -> None:
        self._label = label
        self._open = default_open

        self._tag: ItemTag = dpg.generate_uuid()
        self._header: ItemTag = dpg.generate_uuid()
        self._header_icon: ItemTag = dpg.generate_uuid()
        self._header_label: ItemTag = dpg.generate_uuid()
        self._body: ItemTag = dpg.generate_uuid()

        ICON_PADDING_LEFT: int = 8
        ICON_TO_TEXT_SPACING: int = 6

        with dpg.child_window(tag=self._tag, auto_resize_y=True):
            with dpg.group(
                tag=self._header,
                horizontal=True,
                horizontal_spacing=ICON_TO_TEXT_SPACING,
            ):
                dpg.add_selectable(
                    label=(Icon.CHEVRON_DOWN if self._open else Icon.CHEVRON_RIGHT),
                    tag=self._header_icon,
                    indent=ICON_PADDING_LEFT,
                    height=40,
                    callback=self._toggle,
                )
                dpg.add_button(
                    label=label,
                    height=40,
                    tag=self._header_label,
                )
            dpg.add_child_window(tag=self._body, auto_resize_y=True)

        ThemeManager.subscribe(self)

    @property
    def body(self) -> ItemTag:
        return self._body

    def __enter__(self) -> CollapsiblePanel:
        dpg.push_container_stack(self._body)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        dpg.pop_container_stack()

    def apply_theme(self) -> None:
        dpg.bind_item_font(self._header_icon, ThemeManager.icon_font())
        dpg.bind_item_theme(
            self._tag,
            ThemeManager.item_theme(componentTheme=ComponentTheme.COLLAPSIBLE_PANEL),
        )
        dpg.bind_item_theme(
            self._header,
            ThemeManager.item_theme(
                componentTheme=ComponentTheme.COLLAPSIBLE_PANEL_HEADER
            ),
        )
        dpg.bind_item_theme(
            self._body,
            ThemeManager.item_theme(
                componentTheme=ComponentTheme.COLLAPSIBLE_PANEL_BODY
            ),
        )

    def _toggle(self) -> None:
        self._open = not self._open
        dpg.set_item_label(
            self._header_icon,
            label=Icon.CHEVRON_DOWN if self._open else Icon.CHEVRON_RIGHT,
        )
        dpg.configure_item(
            self._body,
            show=self._open,
        )
