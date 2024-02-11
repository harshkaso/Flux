import dearpygui.dearpygui as dpg
from math import sqrt
class Particle:
    def __init__(self, pos=[0,0], vel=[0,0], acc=[0,0]) -> None:
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.p = None

    def update(self):
        self.vel = self.clamp([self.vel[0] + self.acc[0], self.vel[1] + self.acc[1]], 4)
        self.pos = [self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]]
        self.acc = [0,0]
        dpg.configure_item(self.p, center = self.pos)

    def apply_force(self, force):
        self.acc = [self.acc[0] + force[0], self.acc[1] + force[1]]
    
    def show(self):
        self.p = dpg.draw_circle(center=self.pos, radius=3, fill=[255,255,255,255])

    def warp_around_edges(self, width, height):
        if self.pos[0] > width-1: self.pos[0] = 0 
        if self.pos[0] < 0: self.pos[0] = width - 1
        if self.pos[1] > height-1: self.pos[1] = 0 
        if self.pos[1] < 0: self.pos[1] = height - 1


    def follow(self, vectors, cols, scale):
        x = (self.pos[0] // scale) % cols
        y = self.pos[1] // scale
        idx = int(x + y * cols)
        try:
            force = vectors[idx]
        except Exception:
            print(vectors)
            print(len(vectors), idx)
            print(x, y, cols)
            print(self.pos)

        self.apply_force(force=force)

    def clamp(self, v, n_max):
        x, y = v
        n = sqrt(x**2 + y**2)
        f = min(n, n_max) / n
        return [f*x, f*y]
