import numpy as np
import config as cfg
from types import SimpleNamespace

def get_flowfield_function_name():
  return  'Swirly'

def flowfield():
  def init_flowfield():
    cfg.reset_particles = cfg.default_reset_particles

  args = SimpleNamespace(
    curviness = SimpleNamespace(
      val = 3.5,
      min_val = 0.0,
      max_val = 20.0
    ),
    scale = SimpleNamespace(
      val = 0.1,
      min_val = 0.001,
      max_val = 0.5
    )
  )
  init_flowfield()
  
  def noise(particles, frame_count):
    nonlocal args
    angles = (np.cos(particles[0]*args.scale.val) + np.sin(particles[1]*args.scale.val)) * args.curviness.val
    return np.cos(angles), np.sin(angles)

  return args, noise

