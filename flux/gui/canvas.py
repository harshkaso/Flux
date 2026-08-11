import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.types import Color, ItemTag
from flux.utils.logger import get_logger

logger = get_logger(__name__)


class Canvas:
    def __init__(self) -> None:
        self._tag: ItemTag = dpg.generate_uuid()
        with dpg.child_window(tag=self._tag):
            ...

    def set_background(self, color: Color) -> None: ...
