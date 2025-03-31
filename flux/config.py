from types import SimpleNamespace

class UITypes:
    SLIDER_INT = 0
    SLIDER_FLOAT = 1
    INPUT_TEXT = 2
    FILE_DIALOG = 3
    
class UIDimensions:
    side_panel_width = 300
    flowfield_width = 1000
    flowfield_height = 750

    viewport_width = flowfield_width + side_panel_width
    viewport_height = flowfield_height

class Colors:
    bg_color = [1, 5, 58]
    particle_color_1 = [0, 255, 255]
    particle_color_2 = [150, 0, 255]
    particle_color_3 = [255, 0, 0]
    particle_alpha = 25
    depth_layer_alpha = 10

class Properties:
    total_particles = SimpleNamespace(value=25000, min_value=0, max_value=50000)
    speed = SimpleNamespace(value=1, min_value=0.1, max_value=4)
    min_age = SimpleNamespace(value=50, min_value=50, max_value=100)
    max_age = SimpleNamespace(value=250, min_value=101, max_value=250)
    radius = SimpleNamespace(value=1, min_value=0, max_value=20, is_random=False)
    mask_fade = SimpleNamespace(value=1, min_value=1, max_value=10)
    assert min_age.max_value < max_age.min_value, "min_age must be less than max_age"

class Defaults:
    flowfield_function = 'FastNoiseSIMD'
    particle_color_function = 'Angle'
    mask = 'Unmasked'

