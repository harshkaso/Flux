import dearpygui.dearpygui as dpg
from config import Colors

import dearcygui as dcg

class StyleManager:
    def __init__(self, context):
        self.regular_font = dcg.AutoFont(context, 13, main_font_path='flux/Space_Mono/SpaceMono-Regular.ttf')
        self.bold_font = dcg.AutoFont(context, 13, main_font_path='flux/Space_Mono/SpaceMono-Bold.ttf')
        self.bold_italic_font = dcg.AutoFont(context, 13, main_font_path='flux/Space_Mono/SpaceMono-BoldItalic.ttf')
        self.italic_font = dcg.AutoFont(context, 13, main_font_path='flux/Space_Mono/SpaceMono-Italic.ttf')


        with dcg.ThemeList(context) as self.app_layout_theme:
            dcg.ThemeStyleImGui(context, ItemSpacing=(0,0), ItemInnerSpacing=(0,0))

        with dcg.ThemeList(context) as self.flowfield_window_theme:
            dcg.ThemeStyleImGui(context, WindowPadding=(0,0))
            self._flowfield_window_colors = dcg.ThemeColorImGui(context, ChildBg=Colors.bg_color)

        with dcg.ThemeList(context) as self.side_panel_theme:
            dcg.ThemeStyleImGui(context)

        with dcg.ThemeList(context) as self.dropdown_btn_theme:
            dcg.ThemeStyleImGui(context, ItemSpacing=(8,10))

        with dcg.ThemeList(context) as self.tab_theme:
            dcg.ThemeStyleImGui(context)

        with dcg.ThemeList(context) as self.properties_theme:
            dcg.ThemeStyleImGui(context, ItemSpacing=(8,4))

    def update_flowfield_window_theme(self, bg_color):
        self._flowfield_window_colors.ChildBg = bg_color

    # @staticmethod
    # def update_app_theme(bg_color=None):
    #     if bg_color != None:
    #         config.Colors.bg_color = [int(c*255) for c in bg_color]
    #     r,g,b,a = config.Colors.bg_color
    #     # Calculate Luminance of background
    #     # Needed for runntime UI themes.
    #     l = 0.2126 * r + 0.7152 * g + 0.0722 * b
    #     threshold = 180
    #     # a = 180
    #     print(r,g,b,a)
    #     with dpg.theme() as global_theme:
    #         with dpg.theme_component(dpg.mvAll):
    #             dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
    #             dpg.add_theme_color(dpg.mvThemeCol_ChildBg, [r,g,b,a], category=dpg.mvThemeCat_Core)
    #             dpg.add_theme_color(dpg.mvThemeCol_Text, [255,255,255,255] if l < threshold else [0,0,0,255], category=dpg.mvThemeCat_Core)
    #             dpg.add_theme_color(dpg.mvThemeCol_FrameBg, [int(r-(r/20)),int(g-(g/20)),int(b-(b/20)),100], category=dpg.mvThemeCat_Core)
    #     dpg.bind_theme(global_theme)
