import dearpygui.dearpygui as dpg
import pyfastnoisesimd as fns
import numpy as np

# CONSTANTS
TAU = np.pi * 2

# CONFIG VARIABLES
ff_width  = 1000        # Flowfield Width
ff_height = 750         # Flowfield Height
n_scale =  0.1         # Noise Scale
ttl_particles = 1000    # Total Particles

bg_color = [1,5,58,255] # Background Color

# CONTAINERS
positions = []          # Particle Positions
particles = []          # Particle Objects

noise = fns.Noise()

def spawn_paricles():
    global positions, ff_width, ff_height, particles, ttl_particles
    positions = np.ndarray((2, ttl_particles))
    positions[0,:] = [np.random.random() * ff_width for _ in range(ttl_particles)]
    positions[1,:] = [np.random.random() * ff_height for _ in range(ttl_particles)]
    # for each coardinates draw a particle
    for i in range(ttl_particles):
        p = positions[:,i]
        particles.append(dpg.draw_circle(center=(p[0], p[1]), radius=1, parent='flowfield', show=False))

def recalc_particles():
    global noise, TAU, positions, particles, ttl_particles, ff_width, ff_height
    coords = fns.empty_coords(ttl_particles)
    coords[0,:] = positions[0,:] * n_scale
    coords[1,:] = positions[1,:] * n_scale
    coords[2,:] = np.repeat(dpg.get_frame_count()*n_scale*n_scale, ttl_particles)
    angles = noise.genFromCoords(coords) * TAU
    for i, a in enumerate(angles):
        p = positions[:,i]
        r = int((p[0] / ff_width) * 255)
        g = int((p[1] / ff_height) * 255)
        b = int((p[0]+1/p[1]+1) * 255)
        o = 50
        dpg.configure_item(particles[i], center=(p[0], p[1]), fill=[r,g,b,o], color=[r,g,b,o], show=True)
        p[0] += np.cos(a)
        p[1] += np.sin(a)
        if not (p[0] > 0 and p[0] < ff_width and p[1] > 0 and p[1] < ff_height):
            p[0] = np.random.random() * ff_width
            p[1] = np.random.random() * ff_height

def background(clr=bg_color[:3], opacity=255):
    global ff_width, ff_height
    clr.append(opacity)
    background = dpg.draw_rectangle(pmin=(0,0), pmax=(ff_width, ff_height), parent='flowfield', fill=clr, color=clr)
    return background

def init_frame_buffer(sender, buffer):
    # Initiate handling of frame buffer
    global ff_width, ff_height, ttl_particles
    # First resolve the dimensions
    with dpg.mutex():
        ff_width = dpg.get_viewport_client_width()
        ff_height = dpg.get_viewport_client_height()
        with dpg.texture_registry():
            dpg.add_raw_texture(width=ff_width, height=ff_height, default_value=buffer, format=dpg.mvFormat_Float_rgba, tag="prev_frame")
        dpg.add_image('prev_frame', width=ff_width, parent='flowfield', pos=(0,0))
        background(opacity=10)
        spawn_paricles()

        dpg.set_frame_callback(dpg.get_frame_count()+1, callback=lambda: dpg.output_frame_buffer(callback=handle_frame_buffer))


def handle_frame_buffer(sender, buffer):
    with dpg.mutex():
        dpg.set_value('prev_frame', buffer)
        recalc_particles()
        dpg.set_frame_callback(dpg.get_frame_count()+2, callback=lambda: dpg.output_frame_buffer(callback=handle_frame_buffer))


def setup_flux():
    # Setup flux window
    dpg.create_context()
    dpg.create_viewport(title='Flux', width=ff_width, height=ff_height, resizable=False)
    dpg.setup_dearpygui()

    with dpg.window(tag='flowfield', pos=(0,0)):
        dpg.set_primary_window('flowfield', True)
        with dpg.theme() as flowfield_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, bg_color, category=dpg.mvThemeCat_Core)
    
        dpg.bind_item_theme('flowfield', flowfield_theme)
    
def start_flux():
    # Start Flux
    setup_flux()
    dpg.show_viewport()
    dpg.set_frame_callback(20, callback=lambda: dpg.output_frame_buffer(callback=init_frame_buffer))
    # dpg.set_frame_callback(20, callback=lambda: dpg.output_frame_buffer(callback=_handle_frame_buffer))
    # dpg.set_viewport_vsync(False)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    start_flux()
