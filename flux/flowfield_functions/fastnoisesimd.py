import pyfastnoisesimd as fns
import numpy as np
import config as cfg
from types import SimpleNamespace

def get_flowfield_function_name():
	return 'FastNoiseSIMD'

def flowfield():
	coords = fns.empty_coords(cfg.max_particles)
	fns_noise = fns.Noise()
	TAU = np.pi * 2

	def init_flowfield():
		cfg.reset_particles = cfg.default_reset_particles
		# cfg.reset_particles(np.repeat(True, cfg.max_particles))

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
	
	init_flowfield()

	def noise(particles, frame_count):
		nonlocal fns_noise, coords, TAU, args
		coords[0] = cfg.particles[0] * args.noise_scale.val
		coords[1] = cfg.particles[1] * args.noise_scale.val
		coords[2] = np.repeat(frame_count, coords[0].size) * args.time_scale.val
		angles = fns_noise.genFromCoords(coords) * TAU
		return np.cos(angles), np.sin(angles)
	return args, noise