import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.types import ItemTag
from flux.theme.models import ThemeSpec


def build_settings_button_normal_theme(theme: ThemeSpec) -> ItemTag:
    with dpg.theme() as theme_tag:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 12)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8, 8)
            dpg.add_theme_color(dpg.mvThemeCol_Border, theme.colors.primary_bg)

    return theme_tag


def build_settings_button_active_theme(theme: ThemeSpec) -> ItemTag:
    with dpg.theme() as theme_tag:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 12)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8, 8)
            # dpg.add_theme_color(dpg.mvThemeCol_ChildBg, theme.colors.primary_bg)
            dpg.add_theme_color(dpg.mvThemeCol_Border, theme.colors.accent)

    return theme_tag
