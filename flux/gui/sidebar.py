import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.types import ItemTag
from flux.utils.logger import get_logger

logger = get_logger(__name__)


class Sidebar:
    def __init__(self) -> None:
        self._window: ItemTag | None = None

    @property
    def window(self) -> ItemTag | None:
        return self._window

    def build(self) -> None:
        if self._window:
            return
        with dpg.child_window(width=150) as self._window:
            dpg.add_text(default_value="Sidebar")
