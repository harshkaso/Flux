import numpy as np
from types import SimpleNamespace


def lorenz_attractor():
  TAU = np.pi * 2
  
  args = SimpleNamespace(
    scale = SimpleNamespace(
      val = 0.005,
      min_val = 0.001,
      max_val = 0.01
    ),
    sigma = SimpleNamespace(
      val = 10,
      min_val = 1,
      max_val = 20
    ),
    rho = SimpleNamespace(
      val = 28,
      min_val = 10,
      max_val = 40
    ),
    beta = SimpleNamespace(
      val = 2.667,
      min_val = 1,
      max_val = 5
    )
  )
  
  def noise(coords):
    nonlocal args, TAU
    x, y, z = coords
    x *= args.scale.val*3.4
    y *= args.scale.val**3
    z *= args.scale.val**5
    x_dot = args.sigma.val*(y - x)
    y_dot = args.rho.val*x - y - x*z
    z_dot = x*y - args.beta.val*z
    return x_dot * y_dot * z_dot

  return args, noise

