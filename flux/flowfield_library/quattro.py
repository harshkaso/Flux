import numpy as np
from config import UITypes, UIDimensions
from types import SimpleNamespace

class Quattro:
    def __init__(self):
        self.name = 'Quattro'
        self.TAU = np.pi * 2
        self.args = SimpleNamespace(
            scale = SimpleNamespace(
                label = 'Scale',
                value = 1500,
                min_value = 500,
                max_value = 5000,
                type = UITypes.SLIDER_FLOAT
            ),
            
            a = SimpleNamespace(
                label = 'A',
                value = 15,
                min_value = 1,
                max_value = 20,
                type = UITypes.SLIDER_FLOAT
            ),
            b = SimpleNamespace(
                label = 'B',
                value = 10,
                min_value = 1,
                max_value = 20,
                type = UITypes.SLIDER_FLOAT
            ),
            n = SimpleNamespace(
                label = 'N',
                value = 6,
                min_value = 1,
                max_value = 10,
                type = UITypes.SLIDER_FLOAT
            ),
            m = SimpleNamespace(
                label = 'M',
                value = 4,
                min_value = 1,
                max_value = 10,
                type = UITypes.SLIDER_FLOAT
            )

        )
        self.init_flowfield()

    def init_flowfield(self):
        self.spawn_coordinates = np.ones((UIDimensions.flowfield_height, UIDimensions.flowfield_width), dtype=bool)


    def get_angles(self, particles, frame_count):
        x, y = np.asarray(particles[:2]/(self.args.scale.value), dtype=np.float32)
        return np.cos(self.TAU*self.args.m.value*x)*np.cos(self.TAU*self.args.n.value*y)*self.args.a.value \
        - np.cos(self.TAU*self.args.n.value*x)*np.cos(self.TAU*self.args.m.value*y)*self.args.b.value

