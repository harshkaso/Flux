import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.types import ItemTag
from flux.theme.models import ThemeSpec


def build_application_theme(theme: ThemeSpec) -> ItemTag:
    with dpg.theme() as theme_tag:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, theme.colors.primary_bg)
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, theme.colors.secondary_bg)
            dpg.add_theme_color(dpg.mvThemeCol_Border, theme.colors.secondary_bg)
            dpg.add_theme_color(dpg.mvThemeCol_Text, theme.colors.primary_text)
            dpg.add_theme_style(dpg.mvStyleVar_ImageBorderSize, 1)
    return theme_tag
