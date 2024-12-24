import numpy as np
import config as cfg
from types import SimpleNamespace

def get_flowfield_function_name():
  return 'Quattro'

def flowfield():
  TAU = np.pi * 2

  def init_flowfield():
    cfg.reset_particles = cfg.default_reset_particles
  
  args = SimpleNamespace(
    scale = SimpleNamespace(
      val = 1500,
      min_val = 500,
      max_val = 5000
    ),
    
    a = SimpleNamespace(
      val = 15,
      min_val = 1,
      max_val = 20
    ),
    b = SimpleNamespace(
      val = 10,
      min_val = 1,
      max_val = 20
    ),
    n = SimpleNamespace(
      val = 6,
      min_val = 1,
      max_val = 10
    ),
    m = SimpleNamespace(
      val = 4,
      min_val = 1,
      max_val = 10
    )
  )

  init_flowfield()
  
  def noise(particles, frame_count):
    nonlocal args, TAU
    x, y = particles[:2, :]/(args.scale.val)
    angles = np.cos(TAU*args.m.val*x)*np.cos(TAU*args.n.val*y)*args.a.val \
      - np.cos(TAU*args.n.val*x)*np.cos(TAU*args.m.val*y)*args.b.val
    return np.cos(angles), np.sin(angles)
  return args, noise

