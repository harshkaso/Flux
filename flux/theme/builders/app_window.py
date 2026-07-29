import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.types import ItemTag
from flux.core.models import ThemeSpec


class AppWindowTheme:
    def __init__(self) -> None:
        pass

    def build(self, theme: ThemeSpec) -> ItemTag:
        with dpg.theme() as t:
            with dpg.theme_component(dpg.mvWindowAppItem):
                dpg.add_theme_color(
                    dpg.mvThemeCol_WindowBg,
                    theme.colors.primary_bg,
                )
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)

        return t
