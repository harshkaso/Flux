import numpy as np

def get_color_function_name():
    return 'Angle'

def color(min_rgb, max_rgb, base_alpha, args):
    angle_norm = np.arctan2(args['dx'], args['dy'])
    r = np.add(min_rgb[0], np.multiply(angle_norm, (max_rgb[0] - min_rgb[0])))
    g = np.add(min_rgb[1], np.multiply(angle_norm, (max_rgb[1] - min_rgb[1])))
    b = np.add(min_rgb[2], np.multiply(angle_norm, (max_rgb[2] - min_rgb[2])))
    a = np.repeat(base_alpha, r.size)
    return r, g, b, a