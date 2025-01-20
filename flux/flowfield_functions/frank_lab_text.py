import numpy as np
import config as cfg
from PIL import Image, ImageDraw, ImageFont
from types import SimpleNamespace
from utils.flowfield import initialize

def radial_gradient(i, center, c1, c2, bbox):
	mask = Image.new('L',  i.size, 0)
	draw = ImageDraw.Draw(mask)
	draw.rectangle([bbox[0]+cfg.ff_width//2, bbox[1]+cfg.ff_height//2, bbox[2]+cfg.ff_width//2, bbox[3]+cfg.ff_height//2], fill=255)
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

def get_flowfield_function_name():
	return 'Franks Lab Text'

def flowfield():
	previous_angles = None
	w,h = (cfg.ff_width, cfg.ff_height)
	angle_corrector = np.random.random(size=cfg.max_particles)*0.5 + 0.01
	red, green, blue, alpha = None, None, None, None

	text = 'FLUX'
	font_size = 450
	font_path = 'assets/fonts/impact.ttf'

	def set_text(new_text):
		nonlocal text
		text = new_text
		initialize(init_flowfield)

	def set_font_size(new_size):
		nonlocal font_size
		font_size = new_size
		initialize(init_flowfield)

	def set_font_path(new_path):
		nonlocal font_path
		font_path = new_path
		initialize(init_flowfield)

	def init_flowfield():
		nonlocal text, font_size, font_path, w, h, red, green, blue, alpha

		w,h = (cfg.ff_width, cfg.ff_height)
		font = ImageFont.truetype(font_path,size=font_size, encoding='utf-8')
		img = Image.new(mode="RGBA", size=(w,h), color=(0, 0, 0, 0))
		img = radial_gradient(img, (w//2, h//2), (0, 0, 255), (255, 255, 0), font.getbbox(text, anchor='mm'))
		
		font_mask = Image.new('L', (w,h))
		draw = ImageDraw.Draw(font_mask)
		draw.text((w//2, h//2), text, font=font, fill=255, anchor='mm')

		img.putalpha(font_mask)

		red = np.array(img.split()[0])/255.0
		green = np.array(img.split()[1])/255.0
		blue = np.array(img.split()[2])/255.0
		alpha = np.array(img.split()[3])/255.0
		return alpha

	args = SimpleNamespace(
		text = SimpleNamespace(
			val = text,
			callback = lambda sender, data, property: set_text(data),
			type = cfg.TYPE_INPUT_TEXT
		),
		font_size = SimpleNamespace(
			val = 450,
			min_val = 100,
			max_val = 800,
			type = cfg.TYPE_SLIDER_INT,
			callback = lambda sender, data, property: set_font_size(data)
		)
	)

	def noise(particles, frame_count):
		nonlocal previous_angles, args, angle_corrector, w, h, red, green, blue, alpha
		x = np.clip(particles[0].astype(int), 0, w-1)
		y = np.clip(particles[1].astype(int), 0,h-1)

		r = red[y,x]
		g = green[y,x]
		b = blue[y,x]
		a = alpha[y,x]
		
		angles = (2 * np.pi * (r+g+b)/3)*a
		if previous_angles is not None:
			angles = np.select( [angles > previous_angles, angles < previous_angles], 
								[previous_angles + angle_corrector, previous_angles - angle_corrector], angles)
		previous_angles = angles
		dx = np.cos(angles)
		dy = np.sin(angles)
		return dx, dy
	return args, noise, init_flowfield