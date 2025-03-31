import numpy as np
from config import UITypes, UIDimensions
from types import SimpleNamespace

class Spirals:
  def __init__(self):
    self.name = 'Spirals'
    self.args = SimpleNamespace(
      curviness = SimpleNamespace(
        label = 'Curviness',
        value = 10,
        min_value = 1.0,
        max_value = 20.0,
        type = UITypes.SLIDER_FLOAT
      ),
      scale = SimpleNamespace(
        label = 'Scale',
        value = 0.02,
        min_value = 0.001,
        max_value = 0.1,
        type = UITypes.SLIDER_FLOAT
      )
    )
    self.init_flowfield()

  def init_flowfield(self):
    self.spawn_coordinates = np.ones((UIDimensions.flowfield_height, UIDimensions.flowfield_width), dtype=bool)
  

  def get_angles(self, particles, frame_count):
    x, y = np.asarray(particles[:2], dtype=float)
    return (np.cos(x*self.args.scale.value) + np.sin(y*self.args.scale.value)) * (self.args.curviness.value + 1e-10)


