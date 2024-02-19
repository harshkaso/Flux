import math
from random import randrange
from threading import Thread
import threading
import time
import dearpygui.dearpygui as dpg
from opensimplex import noise3, noise3array
from particle import Particle
import numpy as np

_scale = 45
_cols = 20
_rows = 20
particles_total = 500

_width = _cols * _scale
_height = _rows * _scale
_x = np.array([i/_cols for i in range(_cols)])
_y = np.array([i/_cols for i in range(_rows)])
_bg_color = [0,0,0,255]
dpg.create_context()
dpg.create_viewport(title='Custom Title', width=_width+32, height=_height+50, resizable=False)
dpg.setup_dearpygui()

z = 0
inc = 0.01

flowfield = []
# TODO: do we really need the lock? Most probably not.
ff_lock = threading.Lock()
ff_updating = True

def flowfield_update_loop():
    global flowfield, z, ff_updating
    # update 5 times per second
    interval = 0.2
    while ff_updating:
        new_ff = _flowfield((_rows, _cols), z)
        with ff_lock:
            flowfield = new_ff
            z += inc
        time.sleep(interval)


def recalc_particles():
    global flowfield
    with ff_lock:
        cur_flowfield = flowfield
    for particle in particles:
        x = (particle.pos[0] // _scale) % _cols
        y = particle.pos[1] // _scale
        idx = int(x + y * _cols)
        try:
            force = cur_flowfield[idx]
            particle.follow(force)
        except Exception as e:
            print(e)
        particle.age += 1
        if particle.age > particle.max_age:
            particle.age = 0
            particle.max_age = randrange(50, 150)
            particle.pos = [np.random.random() * _width, np.random.random() * _height]

        particle.update()
        particle.warp_around_edges(_width, _height)

# `dpg.set_frame_callback` appears to be unreliable.  If for some reason it misses
# the frame, our animation will stop.  That's why we use a "visible" handler instead,
# and check the frame number explicitly.
next_capture_frame = 0

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
                dpg.add_image('prev_frame', before="draw-area", pos=(0,0))
            
            # We've stored current picture into the background texture and
            # are now ready to move particles around.
            recalc_particles()
            # Run the next update as soon as we can - something needs an extra frame
            # to render correctly; might be the texture.  That's why we skip a frame.
            global next_capture_frame
            next_capture_frame = dpg.get_frame_count()+2

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


# Initialize the flow field
flowfield = _flowfield((_rows, _cols), z)


def _background(clr=_bg_color[:3], opacity=255):
    x, y = _width, _height
    clr.append(opacity)
    background = dpg.draw_rectangle(pmin=(0,0), pmax=(x, y), fill=clr, color=clr)
    return background


horz_angle = 0.0
vert_angle = 0.0
drag_horz_angle = 0.0
drag_vert_angle = 0.0


def set_3d_transform(h_rot, v_rot):
    view_dist = 50
    scale = view_dist/_height
    mat = (
        dpg.create_perspective_matrix(math.pi/2, _width/_height, 1, 100) * 
        dpg.create_fps_matrix([0, 0, view_dist], 0, 0) *
        dpg.create_rotation_matrix(h_rot, (0, 1, 0)) *
        dpg.create_rotation_matrix(v_rot, (1, 0, 0)) *
        dpg.create_scale_matrix((scale, scale, scale)) *
        dpg.create_translation_matrix((-_width/2, -_height/2, 0))
    )
    dpg.apply_transform("transform", mat)


def on_mouse_move(sender, app_data):
    rotation_sens = 0.005
    global horz_angle, vert_angle, drag_horz_angle, drag_vert_angle
    drag_horz_angle = horz_angle + rotation_sens * app_data[1]
    drag_vert_angle = vert_angle + rotation_sens * app_data[2]

    set_3d_transform(drag_horz_angle, drag_vert_angle)


def on_mouse_up():
    global horz_angle, vert_angle, drag_horz_angle, drag_vert_angle
    horz_angle = drag_horz_angle
    vert_angle = drag_vert_angle


def sched_next_capture():
    global next_capture_frame
    with dpg.mutex():
        if next_capture_frame and dpg.get_frame_count() >= next_capture_frame:
            next_capture_frame = 0
            dpg.output_frame_buffer(callback=_handle_frame_buffer)

with dpg.item_handler_registry() as handlers:
    dpg.add_item_visible_handler(callback=sched_next_capture)

with dpg.window(label="FlowField", tag='flowfield', width=_width, height=_height):
    dpg.set_primary_window('flowfield', True)
    dpg.bind_item_handler_registry(dpg.last_item(), handlers)
    
    with dpg.theme() as flowfield_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, _bg_color, category=dpg.mvThemeCat_Core)
    dpg.bind_item_theme('flowfield', flowfield_theme)


    with dpg.handler_registry():
        dpg.add_mouse_drag_handler(button=dpg.mvMouseButton_Left, callback=on_mouse_move)
        dpg.add_mouse_release_handler(button=dpg.mvMouseButton_Left, callback=on_mouse_up)

    show_axes = False
    show_outer_bounds = True
    with dpg.drawlist(pos=(0,0), width=_width, height=_height, tag="draw-area"):
        # Adding a dimmer - once and for good
        _background(opacity=10)
        with dpg.draw_layer(tag="layer", perspective_divide=True):
            with dpg.draw_node(tag="transform"):
                if show_axes:
                    with dpg.draw_node():
                        dpg.apply_transform(dpg.last_item(), dpg.create_translation_matrix((_width/2, _height/2, 0)))
                        dpg.draw_line((-1000, 0, 0), (1000, 0, 0), color=(255, 0, 0))
                        dpg.draw_line((0, -1000, 0), (0, 1000, 0), color=(0, 255, 0))
                        dpg.draw_line((0, 0, -1000), (0, 0, 1000), color=(0, 0, 255))
                if show_outer_bounds:
                    with dpg.draw_node():
                        dpg.draw_quad((0, 0, 0), (_width, 0, 0), (_width, _height, 0), (0, _height, 0), color=(255, 255, 255))

            dpg.set_clip_space("layer", 0, 0, _width, _height, -1.0, 1.0)
            set_3d_transform(horz_angle, vert_angle)

    particles = [ Particle(parent = 'transform', pos = [np.random.random() * _width, np.random.random() * _height], max_age=randrange(50, 150)) for i in range(particles_total) ]


dpg.show_viewport()
Thread(target=flowfield_update_loop).start()
dpg.set_frame_callback(20, callback=lambda: dpg.output_frame_buffer(callback=_handle_frame_buffer))
# dpg.show_metrics()
dpg.start_dearpygui()
# dpg.set_viewport_vsync(False)

ff_updating = False

dpg.destroy_context()