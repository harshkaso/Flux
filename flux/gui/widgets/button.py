from typing import Any, Callable

import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.enums import IconID
from flux.core.protocols import IconProvider
from flux.core.types import ItemTag
from flux.gui.icons.models import IconAsset
from flux.gui.widgets.icon import IconWidget
from flux.utils.logger import get_logger

logger = get_logger(__name__)


class ButtonWidget:
    def __init__(
        self,
        *,
        label: str | None = None,
        icon: IconID | None = None,
        icon_provider: IconProvider | None = None,
        callback: Callable[[], None] | None = None,
    ) -> None:
        if icon is None and label is None:
            logger.error("ButtonWidget requires either icon or label")
            raise ValueError("ButtonWidget requires either icon or label")

        if icon is not None and icon_provider is None:
            logger.error("icon_provider is required when using an icon")
            raise ValueError("icon_provider is required when using an icon")

        self._tag: ItemTag = dpg.generate_uuid()
        self._label_tag: ItemTag = dpg.generate_uuid()
        self._handler_registry: ItemTag = dpg.generate_uuid()
        self._callback: Callable[[], None] | None = callback
        with dpg.group(tag=self._tag, horizontal=True):
            if icon and icon_provider:
                self._icon = IconWidget(icon=icon, icon_provider=icon_provider)
            if label:
                dpg.add_text(tag=self._label_tag, default_value=label)
        self.bind_handlers()

    def bind_handlers(self) -> None:
        with dpg.item_handler_registry(tag=self._handler_registry):
            # dpg.add_item_hover_handler(callback=self._handle_hover)
            dpg.add_item_clicked_handler(callback=self._handle_click)
        dpg.bind_item_handler_registry(self._tag, self._handler_registry)

    def _handle_click(self, sender: ItemTag, app_data: Any) -> None:
        if self._callback:
            self._callback()

    def update_label(self, label: str) -> None:
        dpg.set_value(self._tag, label)

    def update_icon(self, icon: IconID) -> None:
        self._icon.update(icon)
