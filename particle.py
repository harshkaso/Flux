import dearpygui.dearpygui as dpg
import numpy as np

class Particle:
    def __init__(self, parent, pos=[0.0, 0.0], vel=[0.0, 0.0], acc=[0.0, 0.0]) -> None:
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.acc = np.array(acc)
        self.prev_pos = np.array(pos)
        self.parent = parent
        self.p = None
        self._speed_limit = 5

    def update(self, acc_rand:bool=True):
        self.prev_pos = self.pos.copy()
        self.vel += self.acc
        if acc_rand:
            self.vel += [0.025 - np.random.random() * 0.05, 0.025 - np.random.random() * 0.05]
        self.vel = self.clamp(self.vel, self._speed_limit)
        self.pos += self.vel
        r = 128 + int((self.vel[0] / self._speed_limit) * 128)
        g = 128 + int((self.vel[1] / self._speed_limit) * 128)
        color = [ r, g, 255, int((r + g) * 0.5) ]
        if self.p:
            dpg.configure_item(self.p, p1=self.pos, p2=self.prev_pos, color=color)
        else:
            self.p = dpg.draw_line(p1=self.pos, p2=self.prev_pos, color=[0,0,0,255], parent=self.parent)
        self.acc *= (np.random.random() * 0.85)
        return self.p

    def warp_around_edges(self, width, height):
        self.pos[0] = (self.pos[0] + width) % width
        self.pos[1] = (self.pos[1] + height) % height

    def apply_force(self, force):
        self.acc += force

    def clamp(self, v, n_max):
        n = np.linalg.norm(v)
        if n > n_max:
            v *= (n_max / n)
        return v