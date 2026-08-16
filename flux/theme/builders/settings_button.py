import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.types import ItemTag
from flux.theme.models import ThemeSpec


def build_settings_button_normal_theme(theme: ThemeSpec) -> ItemTag:
    with dpg.theme() as theme_tag:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 12)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
            dpg.add_theme_color(dpg.mvThemeCol_Button, theme.colors.primary_bg)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, theme.colors.surface)
            dpg.add_theme_color(
                dpg.mvThemeCol_ButtonHovered, theme.colors.surface_hover
            )

    return theme_tag


def build_settings_button_active_theme(theme: ThemeSpec) -> ItemTag:
    with dpg.theme() as theme_tag:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 12)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1)
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_Border, theme.colors.accent)
            dpg.add_theme_color(dpg.mvThemeCol_Button, theme.colors.primary_bg)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, theme.colors.surface)
            dpg.add_theme_color(
                dpg.mvThemeCol_ButtonHovered, theme.colors.surface_hover
            )

    return theme_tag
