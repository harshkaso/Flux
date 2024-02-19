import dearpygui.dearpygui as dpg
import numpy as np

class Particle:
    def __init__(self, parent, pos=[0.0,0.0], vel=[0.0,0.0], acc=[0.0,0.0], max_age=100) -> None:
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.acc = np.array(acc)
        self.parent = parent
        self.p = None
        self.age = 0
        self.max_age = max_age

    def update(self):
        prev_pos = np.copy(self.pos)
        self.vel += self.acc
        self.vel = self.clamp(self.vel, 4)
        self.pos += self.vel
        self.acc = np.array([0.0,0.0])
        # self.p = dpg.draw_circle(center=self.pos, radius=3, fill=[255,255,255,50], color=[255,255,255,50], parent=self.parent)
        rel_age = self.age/self.max_age

        # Here are various formulas I tried on brightness and color
        # brightness = (1-cos(2*rel_age*math.pi))/2*255
        # sat = 255 * min(1, 16*(rel_age-0.5)**2)
        # sat = 255 * (1-rel_age**2)
        # sat = 255 * (max(0, 8*(0.5-rel_age)**3))
        brightness = 255 * (1-16*(rel_age-0.5)**4)
        sat = 255 * ((1-rel_age)**3)
        if self.p:
            dpg.configure_item(self.p, p1=self.pos, p2=prev_pos, color=(255, sat, 0, brightness))
        else:
            self.p = dpg.draw_line(p1=self.pos, p2=prev_pos, color=(255, sat, 0, brightness), parent=self.parent)
        return self.p
    
    def apply_force(self, force):
        self.acc += force
    
    def warp_around_edges(self, width, height):
        if self.pos[0] >= width or self.pos[0] < 0:
            self.pos[0] = (self.pos[0] + width) % width

        if self.pos[1] >= height or self.pos[1] < 0:
            self.pos[1] = (self.pos[1] + height) % height


    def follow(self, force):

        self.apply_force(force=force)

    def clamp(self, v, n_max):
        n = float(np.sqrt(np.sum(v**2)))
        if n > n_max:
            v *= (n_max/n)
        return v
        # f = min(n, n_max) / n
        # return [f*x, f*y]
 