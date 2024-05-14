import pyfastnoisesimd as fns
import numpy as np
from types import SimpleNamespace


def default_noise():
    args = SimpleNamespace()
    fns_noise = fns.Noise()
    TAU = np.pi * 2
    def noise(coords):
        nonlocal fns_noise, TAU, args
        return fns_noise.genFromCoords(coords) * TAU
    return args, noise