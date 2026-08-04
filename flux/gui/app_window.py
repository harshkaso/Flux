import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.types import ItemTag
from flux.gui.canvas import Canvas
from flux.gui.sidebar import Sidebar
from flux.utils.logger import get_logger
from flux.core.protocols import AppContext
from flux.core.enums import ComponentTheme

logger = get_logger(__name__)


class AppWindow:
    def __init__(self, app: AppContext) -> None:
        self.app = app
        self._tag: ItemTag = dpg.generate_uuid()
        with dpg.window(tag=self._tag):
            with dpg.group(horizontal=True, horizontal_spacing=0.0):
                self.sidebar: Sidebar = Sidebar(self.app)
                self.canvas: Canvas = Canvas(self.app)
        self.app.theme.subscribe(subscriber=self)
        self.apply_theme()

    @property
    def tag(self) -> ItemTag:
        return self._tag

    def apply_theme(self) -> None:
        dpg.bind_item_theme(
            self._tag, self.app.theme.item_theme(ComponentTheme.APP_WINDOW)
        )
