import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.types import ItemTag
from flux.core.models import ThemeSpec


def build_app_window_theme(theme: ThemeSpec) -> ItemTag:
    with dpg.theme() as theme_tag:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
    return theme_tag
