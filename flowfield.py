import dearpygui.dearpygui as dpg
from opensimplex import noise3, noise3array
from particle import Particle
import numpy as np

_scale = 50
_cols = 20
_rows = 10
_width = _cols * _scale
_height = _rows * _scale
_x = np.array([i/_cols for i in range(_cols)])
_y = np.array([i/_cols for i in range(_rows)])
_bg_color = [0,0,0,255]
dpg.create_context()
dpg.create_viewport(title='Custom Title', width=_width, height=_height, resizable=False)
dpg.setup_dearpygui()



def _handle_frame_buffer(sender, buffer):
    with dpg.mutex():
        if dpg.does_item_exist("flowfield"):
            try:
                dpg.set_value('prev_frame', buffer)
            except Exception:
                with dpg.texture_registry():
                    width = dpg.get_viewport_client_width()
                    height = dpg.get_viewport_client_height()
                    dpg.add_raw_texture(width=width, height=height, default_value=buffer, format=dpg.mvFormat_Float_rgba, tag="prev_frame")
                dpg.add_image('prev_frame', parent='flowfield', pos=(0,0))

def _discard(trash):
    with dpg.mutex(): # added this after i suspected dpg was skipping every other frame, not sure if its needed
        for x in trash:
            if dpg.does_item_exist(x):
                dpg.delete_item(x)

def _flowfield(dim, z):
    rows, cols = dim
    flowfield = [None] * rows * cols
    for y in range(rows):
        for x in range(cols):
            idx = x + y * cols
            r = noise3(x/cols, y/rows, z)
            angle = r * np.pi * 2
            flowfield[idx] = (np.cos(angle), np.sin(angle))
    return flowfield

def _background(clr=_bg_color[:3], opacity=255):
    x, y = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    clr.append(opacity)
    background = dpg.draw_rectangle(pmin=(0,0), pmax=(x, y), parent='flowfield', fill=clr, color=clr)
    return background


with dpg.window(label="FlowField", tag='flowfield', width=_width, height=_height):
    dpg.set_primary_window('flowfield', True)
    
    with dpg.theme() as flowfield_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, _bg_color, category=dpg.mvThemeCat_Core)
    dpg.bind_item_theme('flowfield', flowfield_theme)

    particles = [None] * 100
    for i in range(len(particles)):
        particles[i] = Particle(parent = 'flowfield', pos = [np.random.random() * _width, np.random.random() * _height])
        # _trash.append(particles[i].show())


dpg.show_viewport()
# dpg.show_metrics()
# dpg.set_viewport_vsync(False)
z = 0
inc = 0.001
_trash = []
while dpg.is_dearpygui_running():
    if dpg.get_frame_count() > 20:
        dpg.output_frame_buffer(callback=_handle_frame_buffer)
        _discard(_trash)
        _trash = []
        flowfield = _flowfield((_rows, _cols), z)
        _trash.append(_background(opacity=10))
        for particle in particles:
            x = (particle.pos[0] // _scale) % _cols
            y = particle.pos[1] // _scale
            idx = int(x + y * _cols)
            try:
                force = flowfield[idx]
                particle.follow(force)
                _trash.append(particle.update())
                particle.warp_around_edges(_width, _height)
            except Exception as e:
                print(e)
        z += inc
    dpg.render_dearpygui_frame()

dpg.destroy_context()