import dearpygui.dearpygui as dpg
from opensimplex import noise3array, random_seed
from particle import Particle
import numpy as np

_scale = 50
_cols = 20
_rows = 10
particles_total = 1000
_two_pi = np.pi * 2

_width = _cols * _scale
_height = _rows * _scale
_x = np.arange(_cols)/_cols
_y = np.arange(_rows)/_rows
_bg_color = [1,5,58,255]

random_seed()
dpg.create_context()
dpg.create_viewport(title='Flux', width=_width, height=_height, resizable=False)
dpg.setup_dearpygui()

z = 0
inc = 0.001

flowfield = []
flowfield_z = -1

def recalc_particles():
    global z, inc, flowfield, flowfield_z
    if z - flowfield_z >= 0.01:
        flowfield = _flowfield(z)
        flowfield_z = z
    for particle in particles:
        x = (particle.pos[0] // _scale) % _cols
        y = particle.pos[1] // _scale
        angle = flowfield[int(y)][int(x)]
        particle.apply_force(np.array([np.cos(angle), np.sin(angle)]))
        particle.update_properties()
    z += inc


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
                dpg.add_image('prev_frame', parent='flowfield', pos=(0,0))
                # Adding a dimmer - once and for good
                _background(opacity=10)
                
            # We've stored current picture into the background texture and
            # are now ready to move particles around.
            recalc_particles()
            # Run the next update as soon as we can - something needs an extra frame
            # to render correctly; might be the texture.  That's why we skip a frame.
            dpg.set_frame_callback(dpg.get_frame_count()+2, callback=lambda: dpg.output_frame_buffer(callback=_handle_frame_buffer))

def _flowfield(z):
    global _x, _y, _two_pi
    return noise3array(_x, _y, np.array([z]))[0] * _two_pi


def _background(clr=_bg_color[:3], opacity=255):
    x, y = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    clr.append(opacity)
    background = dpg.draw_rectangle(pmin=(0,0), pmax=(x, y), parent='flowfield', fill=clr, color=clr)
    return background


def _key_press(sender, key):
    if key == dpg.mvKey_R:
        random_seed()
        for particle in particles:
            particle.lifespan = 0

def _mouse_move(sender, pointer_coord):
    if dpg.is_item_hovered('flowfield'):
        print(pointer_coord)

with dpg.window(label="FlowField", tag='flowfield', width=_width, height=_height):
    dpg.set_primary_window('flowfield', True)
    particles = np.array([ Particle(parent = 'flowfield', bounds=[_width, _height]) for i in range(particles_total) ])

with dpg.theme() as flowfield_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, _bg_color, category=dpg.mvThemeCat_Core)
dpg.bind_item_theme('flowfield', flowfield_theme)

with dpg.handler_registry():
    dpg.add_key_press_handler(callback=_key_press)

dpg.show_viewport()
dpg.set_frame_callback(20, callback=lambda: dpg.output_frame_buffer(callback=_handle_frame_buffer))
dpg.start_dearpygui()
# dpg.set_viewport_vsync(False)

dpg.destroy_context()