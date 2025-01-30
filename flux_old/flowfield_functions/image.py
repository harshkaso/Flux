import numpy as np
import config as cfg
from types import SimpleNamespace

def get_flowfield_function_name():
	return 'Image'

def flowfield():
	TAU = np.pi * 2

	def init_flowfield():
		return np.ones((cfg.ff_height, cfg.ff_width), dtype=bool)

	args = SimpleNamespace(
		image = SimpleNamespace(
			val = 0.5,
            type = cfg.TYPE_FILE_DIALOG
		)
	)
	
	init_flowfield()

	def noise(particles, frame_count):
		nonlocal TAU, args
		return np.cos(particles[0]), np.sin(particles[1])
	return args, noise, init_flowfield