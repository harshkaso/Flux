import numpy as np

def get_color_function_name():
    return 'Position'

def color(min_rgb, max_rgb, base_alpha, args):
    x_norm = np.divide(args['particles'][0], args['ff_width'])
    y_norm = np.divide(args['particles'][1], args['ff_height'])
    r = np.add(min_rgb[0], np.multiply(x_norm, (max_rgb[0] - min_rgb[0])))
    g = np.add(min_rgb[1], np.multiply(y_norm, (max_rgb[1] - min_rgb[1])))
    b = np.add(min_rgb[2], np.multiply(np.multiply(np.add(x_norm, y_norm), (max_rgb[2] - min_rgb[2])),0.5))
    a = np.repeat(base_alpha, r.size)
    return r, g, b, a
