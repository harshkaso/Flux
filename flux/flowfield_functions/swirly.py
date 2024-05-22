import numpy as np
from types import SimpleNamespace


def swirly():
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
  def noise(coords):
    nonlocal args
    angles = (np.cos(coords[0]*args.scale.val) + np.sin(coords[1]*args.scale.val)) * args.curviness.val
    return np.cos(angles), np.sin(angles)

  return args, noise

