import numpy as np
def color_by_position(props, min_rgb, max_rgb, base_alpha):
    factor_x = np.divide(props['particles'][0], props['ff_width'])
    factor_y = np.divide(props['particles'][1], props['ff_height'])

    r = np.add(min_rgb[0], np.multiply(factor_x, (max_rgb[0] - min_rgb[0])))
    g = np.add(min_rgb[1], np.multiply(factor_y, (max_rgb[1] - min_rgb[1])))
    b = np.add(min_rgb[2], np.multiply(np.multiply(np.add(factor_x, factor_y), (max_rgb[2] - min_rgb[2])),0.5))
    a = np.repeat(base_alpha, props['ttl_particles'])
    return r, g, b, a

