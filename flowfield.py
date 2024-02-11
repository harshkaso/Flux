import dearpygui.dearpygui as dpg
from perlin_noise import PerlinNoise
from opensimplex import noise3
from particle import Particle
from math import pi, cos, sin

import random

# WIDTH = 1000
# HEIGHT = 500
SCALE = 50
COLS = 20
ROWS = 10 

dpg.create_context()
noise = PerlinNoise(octaves=1)

def setup_flowfield(rows, cols, scale):
    recs = [None] * cols * rows
    arws = [None] * cols * rows
    particles = [None] * 500
    with dpg.window(label="FlowField", tag='grid_display', width=cols*scale, height=rows*scale+20):
        with dpg.theme() as grid_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
        dpg.bind_item_theme('grid_display', grid_theme)
        
        with dpg.drawlist(width=cols*scale, height= rows*scale, tag='grid'):
            for y in range(rows):
                for x in range(cols):
                    idx = x + y * cols
                    r = noise3(x/cols, y/rows, 0)
                    clr = [0,0,0,0]
                    recs[idx] = dpg.draw_rectangle(pmin=[x*scale, y*scale], pmax=[(x*scale)+scale, (y*scale)+scale], fill=clr, color=clr)
                    
                    angle = r * pi * 2
                    (dx,dy) = (x*scale + scale*cos(angle),y*scale + scale*sin(angle))
                    arws[idx] = dpg.draw_arrow((dx, dy),(x*scale, y*scale))

            
            for i in range(len(particles)):
                particles[i] = Particle(pos = [random.random() * cols * scale, random.random() * rows * scale])
                particles[i].show()
            return recs, arws, particles 

def _update_noise(dim, noise_map, arws, z, scale):
    rows, cols = dim
    flowfield = [None] * rows * cols
    for y in range(rows):
        for x in range(cols):
            idx = x + y * cols
            # r = noise([x/cols, y/rows, z])
            r = noise3(x/cols, y/rows, z)
            
            clr = [abs(r)*255,abs(r)*255,abs(r)*255,255]
            dpg.configure_item(noise_map[idx], fill =clr, color =clr)
            angle = r * pi * 2 * 4
            flowfield[idx] = (cos(angle), sin(angle))
            (dx,dy) = (x*scale + scale*cos(angle),y*scale + scale*sin(angle))
            dpg.configure_item(arws[idx], p1=(dx, dy), p2=(x*scale, y*scale))
    return flowfield

dpg.create_viewport(title='Custom Title')
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.show_metrics()
dpg.set_viewport_vsync(False)
z = 0
inc = 0.001
recs, arws, particles = setup_flowfield(rows=ROWS, cols=COLS, scale=SCALE)
while dpg.is_dearpygui_running():
    flowfield = _update_noise((ROWS, COLS), recs, arws, z, SCALE)
    for particle in particles:
        particle.follow(flowfield, COLS, SCALE)
        particle.update()
        particle.warp_around_edges(COLS*SCALE, ROWS*SCALE)
    z += inc
    # _update_texture()
    dpg.render_dearpygui_frame()
dpg.destroy_context() 