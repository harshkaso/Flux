import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.protocols import AppContext
from flux.core.types import ItemTag
from flux.utils.logger import get_logger

logger = get_logger(__name__)


class Canvas:
    def __init__(self, app: AppContext) -> None:
        self.app = app
        self._tag: ItemTag = dpg.generate_uuid()
        with dpg.child_window(tag=self._tag, border=False):
            dpg.add_text(default_value="Canvas")
