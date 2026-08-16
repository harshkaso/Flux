from typing import Any, Callable, Optional

import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.enums import Icon
from flux.core.types import ItemTag
from flux.gui.widgets.icon import IconWidget
from flux.theme.manager import ThemeManager
from flux.utils.logger import get_logger

logger = get_logger(__name__)


# class ButtonWidget:
#     def __init__(
#         self,
#         *,
#         label: str | None = None,
#         icon: IconID | None = None,
#         width: int = 0,
#         height: int = 40,
#         callback: Callable[[], None] | None = None,
#     ) -> None:
#         if icon is None and label is None:
#             logger.error("ButtonWidget requires either icon or label")
#             raise ValueError("ButtonWidget requires either icon or label")

#         self._tag: ItemTag = dpg.generate_uuid()
#         self._clickable_tag: ItemTag = dpg.generate_uuid()
#         self._label_tag: ItemTag = dpg.generate_uuid()
#         self._spacer_tag: ItemTag = dpg.generate_uuid()
#         self._handler_registry: ItemTag = dpg.generate_uuid()
#         self._callback: Callable[[], None] | None = callback
#         self._icon: IconWidget | None = None

#         with dpg.table(
#             tag=self._tag,
#             height=height,
#             header_row=False,
#             borders_outerH=True,
#             borders_outerV=True,
#         ):
#             dpg.add_table_column()
#             with dpg.table_row():
#                 with dpg.group(tag=self._clickable_tag, horizontal=True):
#                     if icon:
#                         self._icon = IconWidget(icon=icon)
#                     if label:
#                         dpg.add_button(label=label, tag=self._label_tag, width=-1)
#                         if self._icon:
#                             dpg.configure_item(
#                                 self._label_tag, height=self._icon.height
#                             )
#         ThemeManager.subscribe(self)


#     def _handle_click(self, sender: ItemTag, app_data: Any) -> None:
#         if self._callback:
#             self._callback()

#     def update_label(self, label: str) -> None:
#         dpg.set_value(self._tag, label)

#     def update_icon(self, icon: IconID) -> None:
#         if self._icon:
#             self._icon.update(icon)

#     def apply_theme(self) -> None:
#         dpg.bind_item_theme(
#             self._tag,
#             theme=ThemeManager.item_theme(componentTheme=ComponentTheme.BUTTON),
#         )


class ButtonWidget:
    def __init__(
        self,
        *,
        label: Optional[str] = None,
        icon: Optional[Icon] = None,
        width: Optional[int] = 0,
        height: Optional[int] = 50,
        callback: Optional[Callable] = None,
    ) -> None:
        if icon is None and label is None:
            logger.error("ButtonWidget requires either icon or label")
            raise ValueError("ButtonWidget requires either icon or label")
        with dpg.group(horizontal=True, horizontal_spacing=0):
            ...
