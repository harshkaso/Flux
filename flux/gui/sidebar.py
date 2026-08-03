import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.protocols import AppContext
from flux.core.types import ItemTag
from flux.utils.logger import get_logger

logger = get_logger(__name__)


class Sidebar:
    def __init__(self, app: AppContext, width: int = 300) -> None:
        self.app = app
        self.width = width
        self._window: ItemTag = dpg.generate_uuid()
        with dpg.child_window(tag=self._window, width=self.width):
            dpg.add_text(default_value="Sidebar")
