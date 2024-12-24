import numpy as np
import config as cfg

def get_color_function_name():
    return 'Radius'

def color(min_rgb, max_rgb, base_alpha, args):
    radius_norm = np.divide(args['particles'][7], cfg.radius)
    r = np.add(min_rgb[0], np.multiply(radius_norm, (max_rgb[0] - min_rgb[0])))
    g = np.add(min_rgb[1], np.multiply(radius_norm, (max_rgb[1] - min_rgb[1])))
    b = np.add(min_rgb[2], np.multiply(radius_norm, (max_rgb[2] - min_rgb[2])))
    a = np.repeat(base_alpha, r.size)
    return r, g, b, a