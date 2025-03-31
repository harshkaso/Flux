
import numpy as np
from config import UITypes, UIDimensions
from PIL import Image, ImageDraw, ImageFont
from types import SimpleNamespace

class Text:
    def __init__(self):
        self.name = 'Text'
        self.font_coords = []
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
                value = self.font_size,
                min_value = 100,
                max_value = 800,
                type = UITypes.SLIDER_INT,
                callback = self._set_font_size
            )
        )
        self.init_mask()

    def initialize(self):
        self.font_coords = []
        self.text = 'FLUX'
        self.font_size = 450
        self.font_path = 'assets/fonts/impact.ttf'

    def _set_text(self, new_text):
        self.text = new_text
        self.init_mask()

    def _set_font_size(self, new_size):
        self.font_size = new_size
        self.init_mask()

    def _set_font_path(self, new_path):
        self.font_path = new_path
        self.init_mask()

        

    def init_mask(self):

        w,h = (UIDimensions.flowfield_width, UIDimensions.flowfield_height)
        # cfg.reset_particles = reset_particles
        font = ImageFont.truetype(self.font_path,size=self.font_size, encoding='utf-8')
        img = Image.new(mode="RGBA", size=(w,h), color=(0, 0, 0, 0))        
        font_mask = Image.new('L', (w,h))
        draw = ImageDraw.Draw(font_mask)
        draw.text((w//2, h//2), self.text, font=font, fill=255, anchor='mm')

        img.putalpha(font_mask)
        self.masked_coordinates = np.array(img.split()[3])/255.0