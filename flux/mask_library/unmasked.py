import numpy as np
from config import UIDimensions


class Unmasked:
    def __init__(self):
        self.name = 'Unmasked'
        self.args = None
        self.init_mask()
    
    def init_mask(self):
        self.masked_coordinates = np.ones((UIDimensions.flowfield_height, UIDimensions.flowfield_width))