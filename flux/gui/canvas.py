import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.protocols import AppContext
from flux.core.types import ItemTag
from flux.utils.logger import get_logger

logger = get_logger(__name__)


class Canvas:
    def __init__(self, app: AppContext) -> None:
        self.app = app
        self._window: ItemTag | None = None

    @property
    def window(self) -> ItemTag | None:
        return self._window

    def build(self) -> None:
        if self._window:
            return
        with dpg.child_window(border=False) as self._window:
            dpg.add_text(default_value="Canvas")
