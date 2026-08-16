import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.types import ItemTag
from flux.theme.models import ThemeSpec


def build_collapsible_panel_theme(theme: ThemeSpec) -> ItemTag:
    with dpg.theme() as theme_tag:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 12)
            dpg.add_theme_color(dpg.mvThemeCol_Border, theme.colors.accent)

    return theme_tag


def build_collapsible_panel_header_theme(theme: ThemeSpec) -> ItemTag:
    with dpg.theme() as theme_tag:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_SelectableTextAlign, 0, 0.5)
            dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (0, 0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (0, 0, 0, 0))

            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 0, 0, 0))

            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
    return theme_tag


def build_collapsible_panel_body_theme(theme: ThemeSpec) -> ItemTag:
    with dpg.theme() as theme_tag:
        with dpg.theme_component(dpg.mvAll):
            # Restoring regular child padding on the contents panel
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8, 8)
            # We don't want the border though. Or do we?
            # dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0, 0))
            # No rounding - in case we want the border.
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 0)
            # Making the background transparent: first, the outer child has already
            # filled the background; second, this prevents contents from painting
            # over the parent's border (especially on rounded corners).
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0, 0))
            # Restoring the default spacing
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 4)

    return theme_tag
