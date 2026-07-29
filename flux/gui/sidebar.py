import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.types import ItemTag
from flux.utils.logger import get_logger

logger = get_logger(__name__)


class Sidebar:
    def __init__(self) -> None:
        self.window: ItemTag = dpg.generate_uuid()

    def build(self) -> None:
        with dpg.child_window(tag=self.window):
            dpg.add_text(default_value="Sidebar")
