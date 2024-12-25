import numpy as np
import config as cfg
from types import SimpleNamespace

def get_flowfield_function_name():
	return 'Vortex'

def flowfield():
	def spawn_attractors(sender, data, property):
		nonlocal attractors, rotations, args
		setattr(property, 'val', data)
		attractors = (np.random.rand(data, 2) * (cfg.ff_width, cfg.ff_height)).astype(np.int32)
		rotations = np.random.choice([np.pi / 2, -np.pi / 2], size=(data))

	args = SimpleNamespace(
		points = SimpleNamespace(
			val = 3,
			min_val = 1,
			max_val = 20,
			type = cfg.TYPE_SLIDER_INT,
			callback = spawn_attractors
		)
	)
	attractors = (np.random.rand(args.points.val, 2) * (cfg.ff_width, cfg.ff_height)).astype(np.int32)
	rotations = np.random.choice([np.pi / 2, -np.pi / 2], size=(args.points.val))

	def noise(particles, frame_count):
		nonlocal args, attractors
		vectors = attractors[:, :, np.newaxis] - particles[:2]
		angles = np.arctan2(vectors[:,1,:], vectors[:,0,:]) + rotations[:, np.newaxis]
		weights = 1/np.maximum(np.linalg.norm(vectors, axis=1), 1e-8)
		f_sin = np.sum(np.sin(angles) * weights, axis=0)
		f_cos = np.sum(np.cos(angles) * weights, axis=0)

		# Normalize the resulting angle components
		norm = np.maximum(np.sqrt(f_sin**2 + f_cos**2), 1e-8)
		return f_cos/norm, f_sin/norm
	return args, noise, init_flowfield