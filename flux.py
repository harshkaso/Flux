import dearpygui.dearpygui as dpg
import pyfastnoisesimd as fns
import numpy as np
from presets import color_by_position

# CONSTANTS
TAU = np.pi * 2


# FLOWFIELD CONFIG
sp_width = 250          # Side Panel Width
ff_width  = 1000        # Flowfield Width
ff_height = 750         # Flowfield Height
n_scale = 0.1           # Noise Scale
t_scale = 0.01          # Time Scale

## PARTICLE CONFIG
ttl_particles = 1000    # Total Particles
min_age = 50            # Min Age of Particles
max_age = 250           # Max Age of Particles
speed = 1               # Speed of particles

min_rgb = [58,78,243,255]
max_rgb = [239,217,255,255]

bg_color = [1,5,58,255] # Background Color

# CONTAINERS
particles = np.ndarray((8, ttl_particles))
coords = fns.empty_coords(ttl_particles)

noise = fns.Noise()

def spawn_paricles():
    global ff_width, ff_height, particles, ttl_particles, min_age, max_age
    particles[0,:] = [np.random.random() * ff_width for _ in range(ttl_particles)]  # X
    particles[1,:] = [np.random.random() * ff_height for _ in range(ttl_particles)] # Y
    particles[2,:] = [np.random.randint(min_age, max_age) for _ in range(ttl_particles)] # age
    particles[3,:] = np.repeat(bg_color[0], ttl_particles) # Red
    particles[4,:] = np.repeat(bg_color[1], ttl_particles) # Green
    particles[5,:] = np.repeat(bg_color[2], ttl_particles) # Blue
    particles[6,:] = np.repeat(50, ttl_particles) # Opacity
    # for each coardinates draw a particle
    for p in particles.T:
        p[7] = dpg.draw_circle(center=(p[0], p[1]), radius=1, parent='flowfield', fill=bg_color, color=bg_color, show=True) # Reference to drawn object

def recalc_particles():
    global noise, TAU, coords, particles, ttl_particles, ff_width, ff_height,  min_age, max_age, speed
    coords[0,:] = particles[0,:] * n_scale
    coords[1,:] = particles[1,:] * n_scale
    coords[2,:] = np.repeat(dpg.get_frame_count()*t_scale, ttl_particles)
    angles = noise.genFromCoords(coords) * TAU
    cos_angles = np.cos(angles)
    sin_angles = np.sin(angles)
    particles[0,:] = np.add(particles[0,:], np.multiply(cos_angles, speed))
    particles[1,:] = np.add(particles[1,:], np.multiply(sin_angles, speed))
    particles[2,:] = np.add(particles[2,:], -1)
    particles[3:6,:] = color_by_position(particles, ff_width, ff_height, min_rgb, max_rgb) # RGB
    
    for p in particles.T:
        clr = list(p[3:7])
        if not (0 < p[0] < ff_width and 0 < p[1] < ff_height) or p[2] == 0:
            # if particle is not (on-screen) or age == 0
            # reset the particle 
            p[0] = np.random.random() * ff_width
            p[1] = np.random.random() * ff_height
            p[2] = np.random.randint(min_age, max_age)
        dpg.configure_item(int(p[7]), center=(p[0], p[1]), fill=clr, color=clr)

def background(clr=bg_color[:3], opacity=255):
    global ff_width, ff_height
    clr.append(opacity)
    if dpg.does_item_exist('background'):
        dpg.configure_item('background', fill = clr, color=clr)
    else:
        dpg.draw_rectangle(tag='background', pmin=(0,0), pmax=(ff_width, ff_height), parent='flowfield', fill=clr, color=clr)

def init_frame_buffer(sender, buffer):
    # Initiate handling of frame buffer
    global ff_width, ff_height, ttl_particles
    # First resolve the dimensions
    with dpg.mutex():
        # Window dimensions
        w_height = dpg.get_viewport_client_height()
        w_width = dpg.get_viewport_client_width()
        # Setup Initial Frame
        with dpg.texture_registry():
            dpg.add_raw_texture(width=w_width, height=w_height, default_value=buffer, format=dpg.mvFormat_Float_rgba, tag="prev_frame")
        background(opacity=10)
        dpg.add_image('prev_frame', width=ff_width, parent='flowfield', pos=(0,0), uv_min=(0,0), uv_max=(ff_width/w_width, 1))
        spawn_paricles()
        # Start the frame buffer
        dpg.set_frame_callback(dpg.get_frame_count()+1, callback=lambda: dpg.output_frame_buffer(callback=handle_frame_buffer))


def handle_frame_buffer(sender, buffer):
    with dpg.mutex():
        dpg.set_value('prev_frame', buffer)
        recalc_particles()
        dpg.set_frame_callback(dpg.get_frame_count()+2, callback=lambda: dpg.output_frame_buffer(callback=handle_frame_buffer))


def setup_flux():
    # Setup flux window
    dpg.create_context()
    dpg.create_viewport(title='Flux', width=ff_width+sp_width, height=ff_height, resizable=False)
    dpg.setup_dearpygui()

    # Callbacks
    def set_n_scale(sender, data):
        global n_scale
        n_scale = data

    def set_t_scale(sender, data):
        global t_scale
        t_scale = data

    def set_particle_speed(sender, data):
        global speed
        speed = data

    def set_min_max_age(sender, data):
        global min_age, max_age
        if sender == 'min-age':
            min_age = data
        elif sender == 'max-age':
            max_age = data

    def set_min_max_rgb(sender, data):
        global min_rgb, max_rgb
        if sender == 'min_rgb':
            min_rgb = [int(c*255) for c in data]
        elif sender == 'max_rgb':
            max_rgb = [int(c*255) for c in data]

    def handle_dropdown(sender, data, group):
        if dpg.is_item_shown(group):
            dpg.configure_item(sender, direction=dpg.mvDir_Right)
            dpg.configure_item(group, show=False)
        else:
            dpg.configure_item(sender, direction=dpg.mvDir_Down)
            dpg.configure_item(group, show=True)

    with dpg.window(tag='flowfield', pos=(0,0)):
        dpg.set_primary_window('flowfield', True)
        with dpg.theme() as flowfield_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, bg_color, category=dpg.mvThemeCat_Core)
    
        dpg.bind_item_theme('flowfield', flowfield_theme)

        with dpg.child_window(tag='parameters', pos=(ff_width, 0), width=sp_width, height=-1):
            with dpg.theme() as side_panel_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8)
            dpg.bind_item_theme('parameters', side_panel_theme)
            # Settings for parameters
            dpg.add_spacer(height=3)
            with dpg.group(horizontal=True):
                dpg.add_button(tag='ff-dropdown', arrow=True, direction=dpg.mvDir_Down, callback=handle_dropdown, user_data='flowfield-settings')
                dpg.add_text(default_value='Flowfield Properties')
            with dpg.group(tag='flowfield-settings'):
                dpg.add_slider_float(width=sp_width/2, label='noisescale', min_value=0.05, default_value=n_scale, max_value=3, callback=set_n_scale)
                dpg.add_slider_float(width=sp_width/2, label='timescale', min_value=0, default_value=t_scale, max_value=0.1, callback=set_t_scale)
            dpg.add_separator()
            
            with dpg.group(horizontal=True):
                dpg.add_button(tag='pp-dropdown', arrow=True, direction=dpg.mvDir_Down, callback=handle_dropdown, user_data='particle-settings')
                dpg.add_text(default_value='Particle Properties')
            with dpg.group(tag='particle-settings'):
                dpg.add_slider_float(width=sp_width/2, label='speed', min_value=0.5, default_value=speed, max_value=4, callback=set_particle_speed)
                dpg.add_slider_int(width=sp_width/2, label='min age', tag='min-age', min_value=min_age, default_value=min_age, max_value=100, callback=set_min_max_age)
                dpg.add_slider_int(width=sp_width/2, label='max age', tag='max-age', min_value=101, default_value=max_age, max_value=max_age, callback=set_min_max_age)
                with dpg.group(indent=5, horizontal=True):
                    dpg.add_button(tag='pc-dropdown', arrow=True, direction=dpg.mvDir_Down, callback=handle_dropdown, user_data='particle-color-settings')
                    dpg.add_text(default_value='Particle Color')
                with dpg.group(indent=5, tag='particle-color-settings'):
                    dpg.add_color_picker(width=sp_width/2, label='min_rgb', tag='min_rgb', default_value=min_rgb, no_tooltip=True, callback=set_min_max_rgb)
                    dpg.add_color_picker(width=sp_width/2, label='max_rgb', tag='max_rgb', default_value=max_rgb, no_tooltip=True, callback=set_min_max_rgb)
            dpg.add_separator()

            dpg.add_checkbox(label='Background', default_value=True)
    
def start_flux():
    # Start Flux
    setup_flux()
    dpg.show_viewport()
    dpg.set_frame_callback(20, callback=lambda: dpg.output_frame_buffer(callback=init_frame_buffer))
    # dpg.set_viewport_vsync(False)
    # dpg.show_metrics()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    start_flux()
