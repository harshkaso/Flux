import numpy as np
from types import SimpleNamespace


def chladni_like():
  TAU = np.pi * 2
  
  args = SimpleNamespace(
    scale = SimpleNamespace(
      val = 1.5,
      min_val = 0.1,
      max_val = 5
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

  def noise(coords):
    nonlocal args, TAU
    x, y, z = coords/(args.scale.val*1000)
    angles = np.cos(TAU*args.m.val*x)*np.cos(TAU*args.n.val*y)*args.a.val \
      - np.cos(TAU*args.n.val*x)*np.cos(TAU*args.m.val*y)*args.b.val
    return np.cos(angles), np.sin(angles)
  return args, noise

