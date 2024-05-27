import numpy as np

def get_color_function_name():
    return 'Age'

def color(min_rgb, max_rgb, base_alpha, args):
    age_range = args['max_age'] - args['min_age']
    age_norm = np.divide(np.subtract(args['particles'][2], args['min_age']), age_range)
    r = np.add(min_rgb[0], np.multiply(age_norm, (max_rgb[0] - min_rgb[0])))
    g = np.add(min_rgb[1], np.multiply(age_norm, (max_rgb[1] - min_rgb[1])))
    b = np.add(min_rgb[2], np.multiply(age_norm, (max_rgb[2] - min_rgb[2])))
    a = np.repeat(base_alpha, r.size)
    return r, g, b, a