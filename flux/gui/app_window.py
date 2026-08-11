import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.types import ItemTag
from flux.gui.canvas import Canvas
from flux.gui.sidebar.sidebar import Sidebar
from flux.theme.manager import ThemeManager
from flux.utils.logger import get_logger
from flux.core.enums import ComponentTheme

logger = get_logger(__name__)


class AppWindow:
    def __init__(self) -> None:
        self._tag: ItemTag = dpg.generate_uuid()
        with dpg.window(tag=self._tag):
            with dpg.group(horizontal=True, horizontal_spacing=0.0):
                self.sidebar: Sidebar = Sidebar()
                self.canvas: Canvas = Canvas()
        ThemeManager.subscribe(subscriber=self)

    @property
    def tag(self) -> ItemTag:
        return self._tag

    def apply_theme(self) -> None:
        dpg.bind_item_theme(
            self._tag, ThemeManager.item_theme(ComponentTheme.APP_WINDOW)
        )
