import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.types import ItemTag
from flux.utils.logger import get_logger
from flux.core.protocols import AppContext, Widget, Container
from flux.core.enums import ComponentTheme

logger = get_logger(__name__)


class AppWindow:
    def __init__(self, app: AppContext) -> None:
        self.app = app
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
        self.apply_theme(self.app.theme.item_theme(ComponentTheme.APP_WINDOW))

    def apply_theme(self, theme: ItemTag) -> None:
        if self._window is None:
            logger.warning("cannot app window theme before build().")
            return
        dpg.bind_item_theme(self._window, theme)
