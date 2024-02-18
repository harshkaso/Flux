import dearpygui.dearpygui as dpg
import numpy as np
class Particle:
    def __init__(self, parent, pos=[0.0,0.0], vel=[0.0,0.0], acc=[0.0,0.0]) -> None:
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.acc = np.array(acc)
        self.prev_pos = np.array(pos)
        self.parent = parent
        self.p = None

    def update(self):
        self.prev_pos = np.copy(self.pos)
        self.vel += self.acc
        self.vel = self.clamp(self.vel, 4)
        self.pos += self.vel
        self.acc = np.array([0.0,0.0])
        # self.p = dpg.draw_circle(center=self.pos, radius=3, fill=[255,255,255,50], color=[255,255,255,50], parent=self.parent)
        if self.p:
            dpg.configure_item(self.p, p1=self.pos, p2=self.prev_pos)
        else:
            self.p = dpg.draw_line(p1=self.pos, p2=self.prev_pos, color=[255,255,255,255], parent=self.parent)
        return self.p
    
    def apply_force(self, force):
        self.acc = [self.acc[0] + force[0], self.acc[1] + force[1]]
    
    def warp_around_edges(self, width, height):
        if self.pos[0] > width-1: self.pos[0] = 0 
        if self.pos[0] < 0: self.pos[0] = width-1

        if self.pos[1] > height-1: self.pos[1] = 0 
        if self.pos[1] < 0: self.pos[1] = height-1


    def follow(self, force):

        self.apply_force(force=force)

    def clamp(self, v, n_max):
        n = float(np.sqrt(np.sum(v**2)))
        if n > n_max:
            v *= (n_max/n)
        return v
        # f = min(n, n_max) / n
        # return [f*x, f*y]
 