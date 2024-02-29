import dearpygui.dearpygui as dpg
import pyfastnoisesimd as fns
import numpy as np

# CONSTANTS
TAU = np.pi * 2

# CONFIG VARIABLES
sp_width = 250          # Side Panel Width
ff_width  = 1000        # Flowfield Width
ff_height = 750         # Flowfield Height
n_scale = .1           # Noise Scale
t_scale =  0.01         # Time Scale

## PARTICLE CONFIG
ttl_particles = 1000    # Total Particles
min_age = 150            # Max Age of Particles
max_age = 250           # Min Age of Particles
speed = 1

bg_color = [1,5,58,255] # Background Color

# CONTAINERS
properties = []          # Particle Properties (position, age)
particles = []          # Particle Objects

noise = fns.Noise()

def spawn_paricles():
    global properties, ff_width, ff_height, particles, ttl_particles, min_age, max_age
    properties = np.ndarray((3, ttl_particles))
    properties[0,:] = [np.random.random() * ff_width for _ in range(ttl_particles)]  # X
    properties[1,:] = [np.random.random() * ff_height for _ in range(ttl_particles)] # Y
    properties[2,:] = [np.random.randint(min_age, max_age) for _ in range(ttl_particles)] # age
    # for each coardinates draw a particle
    for i in range(ttl_particles):
        p = properties[:,i]
        particles.append(dpg.draw_circle(center=(p[0], p[1]), radius=1, parent='flowfield', show=False))

def recalc_particles():
    global noise, TAU, properties, particles, ttl_particles, ff_width, ff_height,  min_age, max_age, speed
    coords = fns.empty_coords(ttl_particles)
    coords[0,:] = properties[0,:] * n_scale
    coords[1,:] = properties[1,:] * n_scale
    coords[2,:] = np.repeat(dpg.get_frame_count()*t_scale, ttl_particles)
    angles = noise.genFromCoords(coords) * TAU
    for i, a in enumerate(angles):
        p = properties[:,i]
        r = int((p[0] / ff_width) * 255)
        g = int((p[1] / ff_height) * 255)
        b = int((p[0]+1/p[1]+1) * 255)
        o = 50

        dpg.configure_item(particles[i], center=(p[0], p[1]), fill=[r,g,b,o], color=[r,g,b,o], show=True)
        p[0] += np.cos(a) * speed
        p[1] += np.sin(a) * speed
        p[2] -= 1
        if not (p[0] > 0 and p[0] < ff_width and p[1] > 0) or p[2] == 0:
            p[0] = np.random.random() * ff_width
            p[1] = np.random.random() * ff_height
            p[2] = np.random.randint(min_age, max_age)

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
        dpg.add_image('prev_frame', width=ff_width, parent='flowfield', pos=(0,0), uv_min=(0,0), uv_max=(ff_width/w_width, 1))
        background(opacity=10)
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
    
def start_flux():
    # Start Flux
    setup_flux()
    dpg.show_viewport()
    dpg.set_frame_callback(20, callback=lambda: dpg.output_frame_buffer(callback=init_frame_buffer))
    # dpg.set_frame_callback(20, callback=lambda: dpg.output_frame_buffer(callback=_handle_frame_buffer))
    # dpg.set_viewport_vsync(False)
    dpg.show_metrics()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    start_flux()
