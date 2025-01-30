from types import SimpleNamespace
from abc import ABC, abstractmethod

class UITypes:
    SLIDER_INT = 0
    SLIDER_FLOAT = 1
    INPUT_TEXT = 2
    FILE_DIALOG = 3
    
class UIDimensions:
    side_panel_width = 250
    flowfield_width = 1000
    flowfield_height = 750

    viewport_width = flowfield_width + side_panel_width
    viewport_height = flowfield_height

class UITags:
    app_window = 'app-window'
    side_panel = 'side-panel'
    particles_container = 'particles-container'
    
    flowfield_function_settings = 'flowfield-function-settings'
    
    particle_settings = 'particle-settings'
    total_particles = 'total-particles'
    speed = 'speed'
    min_age = 'min-age'
    max_age = 'max-age'
    random_radius = 'random-radius'
    radius = 'radius'
    
    mask_settings = 'mask-settings'
    
    color_settings = 'color-settings'
    
    

class Colors:
    bg_color = [1, 5, 58, 255]

class ParticleVariables:
    total_particles = SimpleNamespace(value=1500, min_value=0, max_value=5000)
    min_age = SimpleNamespace(value=50, min_value=50, max_value=100)
    max_age = SimpleNamespace(value=250, min_value=101, max_value=250)
    speed = SimpleNamespace(value=1, min_value=0.1, max_value=4)
    radius = SimpleNamespace(value=1, min_value=0, max_value=20)
    random_radius = False
    
    assert min_age.max_value < max_age.min_value, "min_age must be less than max_age"
    
    


class SidePanelMetadata:
    def __init__(self, label, ui_tag, args):
        self.label = label
        self.ui_tag = ui_tag
        self.args = args
