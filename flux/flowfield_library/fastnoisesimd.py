import pyfastnoisesimd as fns
import numpy as np
from config import UIDimensions, Properties, UITypes
from types import SimpleNamespace


class FastNoiseSIMD:
	def __init__(self):
		self.name = 'FastNoiseSIMD'
		self.coords = fns.empty_coords(Properties.total_particles.max_value)
		self.fns_noise = fns.Noise()
		self.TAU = np.pi * 2

		self.args = SimpleNamespace(
			noise_scale = SimpleNamespace(
				label = 'Noise Scale',
				value = 0.2,
				min_value = 0.1,
				max_value = 1,
				type = UITypes.SLIDER_FLOAT
			),
			time_scale = SimpleNamespace(
				label = 'Time Scale',
				value = 0.01,
				min_value = 0,
				max_value = 0.1,
				type = UITypes.SLIDER_FLOAT
			)
		)
		self.init_flowfield()

	def init_flowfield(self):
		self.spawn_coordinates = np.ones((UIDimensions.flowfield_height, UIDimensions.flowfield_width), dtype=bool)
		
	def get_angles(self, particles, frame_count):
		self.coords[0] = particles[0] * self.args.noise_scale.value
		self.coords[1] = particles[1] * self.args.noise_scale.value
		self.coords[2] = np.repeat(frame_count, self.coords[0].size) * self.args.time_scale.value
		return self.fns_noise.genFromCoords(self.coords)*self.TAU
