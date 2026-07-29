import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.types import ItemTag
from flux.utils.logger import get_logger
from flux.core.protocols import Widget, Container

logger = get_logger(__name__)


class AppWindow:
    def __init__(self) -> None:
        self.window: ItemTag = dpg.generate_uuid()

    def build(self, sidebar: Container, canvas: Widget) -> None:
        with dpg.window(tag=self.window, show=True):
            with dpg.group(horizontal=True):
                sidebar.build()
                canvas.build()
