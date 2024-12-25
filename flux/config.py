import pyfastnoisesimd as fns 
import numpy as np

# UI TAGS/IDS
prev_frame_texture = ''
prev_frame = ''
ff_func_settings = 'ff-func-settings'


ff_func = ''                # Flowfield Function
default_fff = 'Franks Lab Text'     # Default Flowfield Function Name

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
particles = np.ndarray((9, max_particles))

# TYPES
TYPE_SLIDER_INT = 'SLIDER_INT'
TYPE_SLIDER_FLOAT = 'SLIDER_FLOAT'
TYPE_INPUT_TEXT = 'INPUT_TEXT'

# DEFAULT FUNCTION DEFINITIONS
def default_reset_particles(reset_indices):
    global particles, ff_width, ff_height, min_age, max_age
    particles[0, reset_indices] = np.multiply(np.random.rand(np.sum(reset_indices)), ff_width)
    particles[1, reset_indices] = np.multiply(np.random.rand(np.sum(reset_indices)), ff_height)
    particles[2, reset_indices] = np.random.randint(min_age, max_age + 1, size=np.sum(reset_indices))


# DEFAULT FUNCTION REFERENCES
reset_particles = default_reset_particles