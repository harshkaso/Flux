
import numpy as np
import config as cfg
from PIL import Image, ImageDraw, ImageFont
from types import SimpleNamespace

def get_mask_function_name():
    return 'Text'

def mask():
    font_coords = []
    text = 'FLUX'
    font_size = 450
    font_path = 'assets/fonts/impact.ttf'

    def set_text(new_text):
        nonlocal text
        text = new_text
        cfg.mask = calc_mask()
        print(cfg.mask.shape)

    def set_font_size(new_size):
        nonlocal font_size
        font_size = new_size
        cfg.mask = calc_mask()

    def set_font_path(new_path):
        nonlocal font_path
        font_path = new_path
        cfg.mask = calc_mask()

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

    def calc_mask():
        nonlocal text, font_size, font_path, font_coords

        w,h = (cfg.ff_width, cfg.ff_height)
        # cfg.reset_particles = reset_particles
        font = ImageFont.truetype(font_path,size=font_size, encoding='utf-8')
        img = Image.new(mode="RGBA", size=(w,h), color=(0, 0, 0, 0))        
        font_mask = Image.new('L', (w,h))
        draw = ImageDraw.Draw(font_mask)
        draw.text((w//2, h//2), text, font=font, fill=255, anchor='mm')

        img.putalpha(font_mask)
        alpha = np.array(img.split()[3])/255.0
        return alpha
    return args, calc_mask