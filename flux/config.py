import pyfastnoisesimd as fns 
import numpy as np

# UI TAGS/IDS
prev_frame_texture = ''
prev_frame = ''
flowfield_container = 'flowfield-container'
particles_container = 'particles-container'
ff_func_settings = 'ff-func-settings'
mask_settings = 'mask-settings'

ff_func = ''                # Flowf 234567ield Function
default_fff = 'Franks Lab Text'     # Default Flowfield Function Name

ff_reset_coords = []        # Flowfield Reset Coords
fade = 1                    # Mask Fade
max_fade = 10               # Max Fade
mask = ''                   # Mask
mask_func = ''              # Mask Function
default_mf = 'Unmasked'     # Default Mask Function Name
clr_func = ''               # Color Function
default_cf = 'Angle'        # Default Color Function Name


sp_width = 300              # Side Panel Width
ff_width  = 1000            # Flowfield Width
ff_height = 750             # Flowfield Height

w_width = ff_width+sp_width # Window Width
w_height = ff_height        # Window Height

max_particles = 5000        # Max number of particles
ttl_particles = 1500        # Total Particles
min_age = 50                # Min Age of Particles
max_age = 250               # Max Age of Particles
speed = 1                   # Speed of particles
radius = 1                  # Radius of particles
max_radius = 20             # Max radius of particles
random_radius = False       # Random Radius


bg_color = [1,5,58,255]     # Background Color
min_rgb = [91,109,255,255]  # Particle Color - Min
max_rgb = [154,0,190,255]   # Particle Color - Max
d_alpha = 10                # Dimmer alpha
p_alpha = 25                # Particle alpha
border = False              # Border of particles
border_rgb = [1,5,58,255]   # Border Color

# CONTAINERS
particles = []            # Particles

# TYPES
TYPE_SLIDER_INT = 'SLIDER_INT'
TYPE_SLIDER_FLOAT = 'SLIDER_FLOAT'
TYPE_INPUT_TEXT = 'INPUT_TEXT'