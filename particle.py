import dearpygui.dearpygui as dpg
import numpy as np

class Particle:
    def __init__(self, parent, bounds, pos=None, vel=[0.0, 0.0], acc=[0.0, 0.0], max_age=255, max_speed=5) -> None:
        self.horz_limit, self.vert_limit = bounds
        if pos == None:
            self.pos = np.array([np.random.random()*self.horz_limit, np.random.random()*self.vert_limit])
        else:
            self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.acc = np.array(acc)
        self.prev_pos = np.array(pos)
        self.max_age = max_age
        self.lifespan = np.random.randint(max_age-1) + 1

        self.parent = parent
        self._speed_limit = max_speed
        self.p = None

    def update(self, acc_rand:bool=True):
        self.lifespan -= 1
        if self.lifespan > 0:
            self.prev_pos = self.pos.copy()
            self.vel += self.acc
            if acc_rand:
                self.vel += [0.025 - np.random.random() * 0.05, 0.025 - np.random.random() * 0.05]
            self.vel = self.clamp(self.vel, self._speed_limit)
            self.pos += self.vel
        else:
            self.pos = np.array([np.random.random()*self.horz_limit, np.random.random()*self.vert_limit])
            self.prev_pos = self.pos.copy()
            self.vel = np.array([0.0,0.0])
            self.lifespan = self.max_age
        r = 128 + int((self.vel[0] / self._speed_limit) * 128)
        g = 128 + int((self.vel[1] / self._speed_limit) * 128)
        color = [ r, g, 255, int((r + g) * 0.5) ]
        # color = [ r, g, 255, (255/self.max_age)*self.lifespan]
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