import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.types import ItemTag
from flux.theme.models import ThemeSpec


def build_settings_rail_theme(theme: ThemeSpec) -> ItemTag:
    with dpg.theme() as theme_tag:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8, 8)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 20)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 15)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, theme.colors.primary_bg)

    return theme_tag
