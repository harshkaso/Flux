import numpy as np
from types import SimpleNamespace


def swirly():
  args = SimpleNamespace(
    curviness = SimpleNamespace(
      val = 3.5,
      min_val = 0.0,
      max_val = 10.0
    )
  )
  
  def noise(coords):
    nonlocal args
    angles = (np.cos(coords[0]) + np.sin(coords[1])) * args.curviness.val
    return angles

  return args, noise

