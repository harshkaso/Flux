import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.enums import ComponentTheme, SettingsPage
from flux.core.types import ItemTag
from flux.core.protocols import SettingsView
from flux.theme.manager import ThemeManager
from flux.gui.sidebar.pages.flowfielld_settings import FlowfieldSettings
from flux.gui.sidebar.pages.particle_settings import ParticleSettings
from flux.gui.sidebar.pages.general_settings import GeneralSettings
from flux.gui.sidebar.pages.mask_settings import MaskSettings
from flux.gui.sidebar.pages.color_settings import ColorSettings
from flux.gui.sidebar.pages.save_settings import SaveSettings


class Inspector:
    def __init__(self) -> None:
        self._tag: ItemTag = dpg.generate_uuid()
        self._active_page: SettingsPage | None = None
        self._visible: bool = True
        with dpg.child_window(tag=self._tag):
            self._pages: dict[SettingsPage, SettingsView] = {
                SettingsPage.FLOWFIELD: FlowfieldSettings(),
                SettingsPage.PARTICLE: ParticleSettings(),
                SettingsPage.MASK: MaskSettings(),
                SettingsPage.COLOR: ColorSettings(),
                SettingsPage.SAVE: SaveSettings(),
                SettingsPage.GENERAL: GeneralSettings(),
            }
        ThemeManager.subscribe(self)

    def set_page(self, page: SettingsPage) -> None:
        if self._active_page is not None:
            dpg.hide_item(self._pages[self._active_page].tag)

        dpg.show_item(self._pages[page].tag)
        self._active_page = page

    def apply_theme(self) -> None:
        dpg.bind_item_theme(
            self._tag, ThemeManager.item_theme(componentTheme=ComponentTheme.INSPECTOR)
        )
