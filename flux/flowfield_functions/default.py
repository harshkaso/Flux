import pyfastnoisesimd as fns
import numpy as np
from types import SimpleNamespace


def default_noise():
	fns_noise = fns.Noise()
	TAU = np.pi * 2

	args = SimpleNamespace(
		noise_scale = SimpleNamespace(
			val = 0.5,
			min_val = 0.1,
			max_val = 3
		),
		time_scale = SimpleNamespace(
			val = 0.01,
			min_val = 0,
			max_val = 0.1
		)
	)
	def noise(coords):
		nonlocal fns_noise, TAU, args
		coords[0] *= args.noise_scale.val
		coords[1] *= args.noise_scale.val
		coords[2] *= args.time_scale.val
		angles = fns_noise.genFromCoords(coords) * TAU
		return np.cos(angles), np.sin(angles)
	return args, noise