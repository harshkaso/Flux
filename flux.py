import dearpygui.dearpygui as dpg
from opensimplex import noise3array, random_seed
from particle import Particle
import numpy as np

TWO_PI = np.pi * 2

flowfield = []

scale = 50
cols = 20
rows = 15

particles_val = 5
particles_mul = 100
ttl_particles = particles_val * particles_mul 
max_particles = 10 # x 100 (multiplier)
min_particles = 2 # x 100 (multiplier)

side_panel_width = 250
flowfield_width = cols * scale
flowfield_height = rows * scale
x_range = np.arange(cols)/cols
y_range = np.arange(rows)/rows
bg_color = [1,5,58,255]

z = 0
inc = 0.001
flowfield_z = -1

random_seed()

def _flowfield(z):
    global x_range, y_range, TWO_PI
    return noise3array(x_range, y_range, np.array([z]))[0] * TWO_PI

def recalc_particles():
    global z, inc, flowfield, flowfield_z
    if z - flowfield_z >= 0.01:
        flowfield = _flowfield(z)
        flowfield_z = z
    for particle in particles[:ttl_particles]:
        x = (particle.pos[0] // scale) % cols
        y = particle.pos[1] // scale
        angle = flowfield[int(y)][int(x)]
        particle.apply_force(np.array([np.cos(angle), np.sin(angle)]))
        particle.update_properties()
    z += inc

def _background(clr=bg_color[:3], opacity=255):
    x, y = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    clr.append(opacity)
    background = dpg.draw_rectangle(tag='background', pmin=(0,0), pmax=(flowfield_width, flowfield_height), parent='flowfield', fill=clr, color=clr)
    return background

def _handle_frame_buffer(sender, buffer):
    with dpg.mutex():
        if dpg.does_item_exist("flowfield"):
            if dpg.does_item_exist('prev_frame'):
                dpg.set_value('prev_frame', buffer)
            else:
                with dpg.texture_registry():
                    width = dpg.get_viewport_client_width()
                    height = dpg.get_viewport_client_height()
                    dpg.add_raw_texture(width=width, height=height, default_value=buffer, format=dpg.mvFormat_Float_rgba, tag="prev_frame")
                dpg.add_image('prev_frame', width=flowfield_width, parent='flowfield', pos=(0,0), uv_min=(0,0), uv_max=(flowfield_width/width, 1))

                # Adding a dimmer - once and for good
                _background(opacity=10)
                
            # We've stored current picture into the background texture and
            # are now ready to move particles around.
            recalc_particles()
            # Run the next update as soon as we can - something needs an extra frame
            # to render correctly; might be the texture.  That's why we skip a frame.
            dpg.set_frame_callback(dpg.get_frame_count()+2, callback=lambda: dpg.output_frame_buffer(callback=_handle_frame_buffer))

def _key_press(sender, key):
    if key == dpg.mvKey_R:
        random_seed()
        for particle in particles:
            particle.lifespan = 0

def show_n_particles(sender, n):
    global particles, ttl_particles, particles_mul
    if sender:
        n *= particles_mul 
        dpg.configure_item(sender, format=n)
    if ttl_particles <= n:
        [particle.show(True) for particle in particles[:n]]
    else:
        [particle.show(False) for particle in particles[n:ttl_particles]]
    ttl_particles = n


def _mouse_move(sender, pointer_coord):
    if dpg.is_item_hovered('flowfield'):
        print(pointer_coord)



dpg.create_context()
dpg.create_viewport(title='Flux', width=flowfield_width + side_panel_width, height=flowfield_height, resizable=False)
dpg.setup_dearpygui()


with dpg.window(label="FlowField", tag='flowfield', pos=(side_panel_width, 0), width=flowfield_width, height=flowfield_height) as flowfield_window:
    dpg.set_primary_window('flowfield', True)
    with dpg.theme() as flowfield_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, bg_color, category=dpg.mvThemeCat_Core)
    dpg.bind_item_theme(flowfield_window, flowfield_theme)
    particles = [ Particle(parent = flowfield_window, bounds=[flowfield_width,flowfield_height], visible=False) for i in range(max_particles*particles_mul) ]
    show_n_particles(None, ttl_particles)

    # Side Panel
    with dpg.child_window(label='Properties', tag='properties', pos=(flowfield_width,0), width=side_panel_width, height=-1):
        with dpg.theme() as flowfield_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8)
        dpg.bind_item_theme('properties', flowfield_theme)
        dpg.add_spacer(height=5)
        dpg.add_slider_int(label='particles', width=150, callback=show_n_particles, default_value=particles_val, max_value=max_particles, min_value=min_particles, format=ttl_particles)
   
with dpg.handler_registry():
    dpg.add_key_press_handler(callback=_key_press)


dpg.show_viewport()
dpg.set_frame_callback(20, callback=lambda: dpg.output_frame_buffer(callback=_handle_frame_buffer))
dpg.set_viewport_vsync(False)
dpg.show_metrics()
dpg.start_dearpygui()

dpg.destroy_context()