import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.types import ItemTag
from flux.utils.logger import get_logger
from flux.core.protocols import Widget, Container
from flux.core.enums import ComponentTheme

logger = get_logger(__name__)


class AppWindow:
    def __init__(self, app) -> None:
        self.app = app
        self.window: ItemTag = dpg.generate_uuid()
        app.theme.subscribe(self)

    def build(self, sidebar: Container, canvas: Widget) -> None:
        with dpg.window(tag=self.window, show=True):
            with dpg.group(horizontal=True, horizontal_spacing=0.0):
                sidebar.build()
                canvas.build()
