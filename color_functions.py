import numpy as np

TAU = np.pi * 2


def color_by_position(props, min_rgb, max_rgb, base_alpha):
    x_norm = np.divide(props['particles'][0], props['ff_width'])
    y_norm = np.divide(props['particles'][1], props['ff_height'])
    r = np.add(min_rgb[0], np.multiply(x_norm, (max_rgb[0] - min_rgb[0])))
    g = np.add(min_rgb[1], np.multiply(y_norm, (max_rgb[1] - min_rgb[1])))
    b = np.add(min_rgb[2], np.multiply(np.multiply(np.add(x_norm, y_norm), (max_rgb[2] - min_rgb[2])),0.5))
    a = np.repeat(base_alpha, props['ttl_particles'])
    return r, g, b, a


def color_by_age(props, min_rgb, max_rgb, base_alpha):
    age_range = props['max_age'] - props['min_age']
    age_norm = np.divide(np.subtract(props['particles'][2], props['min_age']), age_range)
    r = np.add(min_rgb[0], np.multiply(age_norm, (max_rgb[0] - min_rgb[0])))
    g = np.add(min_rgb[1], np.multiply(age_norm, (max_rgb[1] - min_rgb[1])))
    b = np.add(min_rgb[2], np.multiply(age_norm, (max_rgb[2] - min_rgb[2])))
    a = np.repeat(base_alpha, props['ttl_particles'])
    return r, g, b, a

def color_by_angle(props, min_rgb, max_rgb, base_alpha):
    angle_norm = props['angles']
    r = np.add(min_rgb[0], np.multiply(angle_norm, (max_rgb[0] - min_rgb[0])))
    g = np.add(min_rgb[1], np.multiply(angle_norm, (max_rgb[1] - min_rgb[1])))
    b = np.add(min_rgb[2], np.multiply(angle_norm, (max_rgb[2] - min_rgb[2])))
    a = np.repeat(base_alpha, props['ttl_particles'])
    return r,g,b,a


clr_funcs = {
    'Position': color_by_position,
    'Age': color_by_age,
    'Angle': color_by_angle,
}
