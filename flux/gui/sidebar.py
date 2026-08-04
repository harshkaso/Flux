import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.enums import IconID
from flux.core.protocols import AppContext
from flux.core.types import ItemTag
from flux.utils.logger import get_logger
from flux.gui.widgets.icon import IconWidget

logger = get_logger(__name__)


class Sidebar:
    DEFAULT_WIDTH = 300

    def __init__(self, app: AppContext, *, width: int = DEFAULT_WIDTH) -> None:
        self.app = app
        self._width = width
        self._tag: ItemTag = dpg.generate_uuid()
        with dpg.child_window(tag=self._tag, width=width):
            dpg.add_text(default_value="Sidebar")
            icon = IconWidget(icon=IconID.CHEVRON_DOWN, icons=self.app.icons)
