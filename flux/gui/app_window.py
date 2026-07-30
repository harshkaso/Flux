import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.types import ItemTag
from flux.utils.logger import get_logger
from flux.core.protocols import Widget, Container
from flux.core.enums import ComponentTheme

logger = get_logger(__name__)


class AppWindow:
    def __init__(self) -> None:
        self._window: ItemTag | None = None

    @property
    def window(self) -> ItemTag | None:
        return self._window

    def build(self, sidebar: Container, canvas: Widget) -> None:
        if self._window:
            return
        with dpg.window() as self._window:
            with dpg.group(horizontal=True, horizontal_spacing=0.0):
                sidebar.build()
                canvas.build()
