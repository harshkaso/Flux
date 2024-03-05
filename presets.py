import dearpygui.dearpygui as dpg

def color_by_position(p, ff_width, ff_height, min_rgb, max_rgb):
    factor_x = p[0] / ff_width
    factor_y = p[1] / ff_height
    
    r = int(min_rgb[0] + (max_rgb[0] - min_rgb[0]) * factor_x)
    g = int(min_rgb[1] + (max_rgb[1] - min_rgb[1]) * factor_y)
    b = int(min_rgb[2] + (max_rgb[2] - min_rgb[2]) * (factor_x + factor_y) / 2)
    o = 50
    return r, g, b, o