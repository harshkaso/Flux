import numpy as np
from config import UIDimensions, Properties, UITypes
from PIL import Image, ImageDraw, ImageFont
from types import SimpleNamespace

class FrankLabText:
	def __init__(self):
		self.name = 'Franks Lab Text'
		self.previous_angles = None
		self.w,self.h = (UIDimensions.flowfield_width, UIDimensions.flowfield_height)
		self.angle_corrector = np.random.random(size=Properties.total_particles.max_value)*0.5 + 0.01
		self.red, self.green, self.blue, self.alpha = None, None, None, None
		self.text = 'FLUX'
		self.font_size = 450
		self.font_path = 'assets/fonts/impact.ttf'

		self.args = SimpleNamespace(
		text = SimpleNamespace(
			label = 'Text',
			value = self.text,
			callback = self._set_text,
			type = UITypes.INPUT_TEXT
		),
		font_size = SimpleNamespace(
			label = 'Font Size',
			value = 450,
			min_value = 100,
			max_value = 800,
			type = UITypes.SLIDER_INT,
			callback = self._set_font_size
		)
		)
		self.init_flowfield()


		
	def _radial_gradient(self, i, center, c1, c2, bbox):
		mask = Image.new('L',  i.size, 0)
		draw = ImageDraw.Draw(mask)
		draw.rectangle([bbox[0]+self.w//2, bbox[1]+self.h//2, bbox[2]+self.w//2, bbox[3]+self.h//2], fill=255)
		center = np.array(center)
		max_dist = (bbox[2]-bbox[0]) / 2
		if not max_dist:
			return i
		x, y = np.meshgrid(np.arange(i.size[0]), np.arange(i.size[1]))
		c = np.linalg.norm(np.stack((x, y), axis=2) - center, axis=2) / max_dist
		c = np.clip(c, 0, 1)
		c = np.tile(np.expand_dims(c, axis=2), [1, 1, 3])
		c = (c1 * (1 - c) + c2 * c).astype(np.uint8)
		c = Image.fromarray(c)

		i.paste(c, mask=mask)
		return i

	def get_flowfield_function_name(self):
		return 'Franks Lab Text'


	def _set_text(self, new_text):
		self.text = new_text
		self.init_flowfield()

	def _set_font_size(self, new_size):
		self.font_size = new_size
		self.init_flowfield()

	def set_font_path(self, new_path):
		self.font_path = new_path
		self.init_flowfield()
		

	def init_flowfield(self):
		self.w,self.h = (UIDimensions.flowfield_width, UIDimensions.flowfield_height)
		self.font = ImageFont.truetype(self.font_path,size=self.font_size, encoding='utf-8')
		img = Image.new(mode="RGBA", size=(self.w,self.h), color=(0, 0, 0, 0))
		img = self._radial_gradient(img, (self.w//2, self.h//2), (0, 0, 255), (255, 255, 0), self.font.getbbox(self.text, anchor='mm'))
		
		font_mask = Image.new('L', (self.w,self.h))
		draw = ImageDraw.Draw(font_mask)
		draw.text((self.w//2, self.h//2), self.text, font=self.font, fill=255, anchor='mm')

		img.putalpha(font_mask)

		self.red = np.array(img.split()[0])/255.0
		self.green = np.array(img.split()[1])/255.0
		self.blue = np.array(img.split()[2])/255.0
		self.alpha = np.array(img.split()[3])/255.0
		self.spawn_coordinates = self.alpha


	def get_angles(self, particles, frame_count):
		x = np.clip(particles[0].astype(int), 0, self.w-1)
		y = np.clip(particles[1].astype(int), 0,self.h-1)

		r = self.red[y,x]
		g = self.green[y,x]
		b = self.blue[y,x]
		a = self.alpha[y,x]
		
		angles = (2 * np.pi * (r+g+b)/3)*a
		if self.previous_angles is not None:
			angles = np.select( [angles > self.previous_angles, angles < self.previous_angles], 
								[self.previous_angles + self.angle_corrector, self.previous_angles - self.angle_corrector], angles)
		self.previous_angles = angles
		return angles