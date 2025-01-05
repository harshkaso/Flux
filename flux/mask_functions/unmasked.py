
import numpy as np
import config as cfg

def get_mask_function_name():
    return 'Unmasked'

def mask():
    def calc_mask():
        return np.ones((cfg.ff_height,cfg.ff_width)) 
    return None, calc_mask