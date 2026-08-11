import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.enums import ComponentTheme, SettingsPage
from flux.core.types import ItemTag
from flux.gui.sidebar.inspector import Inspector
from flux.gui.sidebar.settings_rail import SettingsRail
from flux.theme.manager import ThemeManager
from flux.utils.logger import get_logger
from flux.gui.widgets.button import ButtonWidget

logger = get_logger(__name__)


class Sidebar:
    DEFAULT_WIDTH = 300

    def __init__(self, *, width: int = DEFAULT_WIDTH) -> None:
        self._width = width
        self._tag: ItemTag = dpg.generate_uuid()
        with dpg.child_window(
            tag=self._tag,
            width=width,
            height=-1,
        ):
            with dpg.group(horizontal=True):
                self.settings_rail = SettingsRail(
                    on_settings_button_selected=self._handle_on_settings_button_selected
                )
                self.inspector = Inspector()
        ThemeManager.subscribe(self)

    def _handle_on_settings_button_selected(self, page: SettingsPage):
        self.inspector.show(page=page)

    def apply_theme(self) -> None:
        dpg.bind_item_theme(
            self._tag, ThemeManager.item_theme(componentTheme=ComponentTheme.SIDEBAR)
        )
