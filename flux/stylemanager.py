import dearpygui.dearpygui as dpg
import globals

class StyleManager:
    @staticmethod
    def update_app_theme(bg_color=None):
        if bg_color != None:
            globals.Colors.bg_color = [int(c*255) for c in bg_color]
        r,g,b,a = globals.Colors.bg_color
        # Calculate Luminance of background
        # Needed for runntime UI themes.
        l = 0.2126 * r + 0.7152 * g + 0.0722 * b
        threshold = 180
        # a = 180
        print(r,g,b,a)
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, [r,g,b,a], category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Text, [255,255,255,255] if l < threshold else [0,0,0,255], category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, [int(r-(r/20)),int(g-(g/20)),int(b-(b/20)),100], category=dpg.mvThemeCat_Core)
        dpg.bind_theme(global_theme)