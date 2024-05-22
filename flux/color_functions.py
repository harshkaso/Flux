import numpy as np

def color_by_position(min_rgb, max_rgb, base_alpha, args):
    x_norm = np.divide(args['particles'][0], args['ff_width'])
    y_norm = np.divide(args['particles'][1], args['ff_height'])
    r = np.add(min_rgb[0], np.multiply(x_norm, (max_rgb[0] - min_rgb[0])))
    g = np.add(min_rgb[1], np.multiply(y_norm, (max_rgb[1] - min_rgb[1])))
    b = np.add(min_rgb[2], np.multiply(np.multiply(np.add(x_norm, y_norm), (max_rgb[2] - min_rgb[2])),0.5))
    a = np.repeat(base_alpha, r.size)
    return r, g, b, a


def color_by_age(min_rgb, max_rgb, base_alpha, args):
    age_range = args['max_age'] - args['min_age']
    age_norm = np.divide(np.subtract(args['particles'][2], args['min_age']), age_range)
    r = np.add(min_rgb[0], np.multiply(age_norm, (max_rgb[0] - min_rgb[0])))
    g = np.add(min_rgb[1], np.multiply(age_norm, (max_rgb[1] - min_rgb[1])))
    b = np.add(min_rgb[2], np.multiply(age_norm, (max_rgb[2] - min_rgb[2])))
    a = np.repeat(base_alpha, r.size)
    return r, g, b, a

def color_by_angle(min_rgb, max_rgb, base_alpha, args):
    angle_norm = np.arctan2(args['dx'], args['dy'])
    r = np.add(min_rgb[0], np.multiply(angle_norm, (max_rgb[0] - min_rgb[0])))
    g = np.add(min_rgb[1], np.multiply(angle_norm, (max_rgb[1] - min_rgb[1])))
    b = np.add(min_rgb[2], np.multiply(angle_norm, (max_rgb[2] - min_rgb[2])))
    a = np.repeat(base_alpha, r.size)
    return r, g, b, a


clr_funcs = {
    'Position': color_by_position,
    'Age': color_by_age,
    'Angle': color_by_angle,
}
