import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.enums import Theme
from flux.core.types import ItemTag
from flux.gui.widgets.collapsible_panel import CollapsiblePanel
from flux.theme.manager import ThemeManager


class GeneralSettings:
    def __init__(self) -> None:
        self._tag: ItemTag = dpg.generate_uuid()
        with dpg.group(tag=self._tag, show=False):
            with CollapsiblePanel(label="Theme Settings"):
                dpg.add_text(default_value="Themes")
                dpg.add_combo(items=[Theme.DARK, Theme.LIGHT], width=-1)

    @property
    def tag(self) -> ItemTag:
        return self._tag
