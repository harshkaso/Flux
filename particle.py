import dearpygui.dearpygui as dpg
import numpy as np

class Particle:
    def __init__(self, parent, bounds, pos=None, vel=[0.0, 0.0], acc=[0.0, 0.0], max_age=150, max_speed=4, mass=2, visible=True) -> None:
        self.horz_limit, self.vert_limit = bounds
        if pos == None:
            self.pos = np.array([np.random.random()*self.horz_limit, np.random.random()*self.vert_limit])
        else:
            self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.acc = np.array(acc)
        self.prev_pos = np.array(pos)
        self.mass = mass
        self.max_age = max_age
        self.lifespan = np.random.randint(50, self.max_age)
        self.age = self.lifespan
        self.parent = parent
        self.speed_limit = max_speed
        self.visible = visible
        self.p = dpg.draw_line(p1=(0,0), p2=(0,0), show=False)

    def show(self, visible):
        if self.visible ^ visible:
            self.visible = visible
            if self.p:
                dpg.configure_item(self.p, show=self.visible)

    def update_properties(self):
        if self.visible:
            self.lifespan -= 1
            if self.lifespan < 1:
                self.max_age = np.random.randint(50,150)
                self.pos = np.array([np.random.random()*self.horz_limit, np.random.random()*self.vert_limit])
                self.lifespan = np.random.randint(10,self.max_age)
                self.age = self.lifespan
                self.vel = np.array([0.0,0.0])
                self.acc = np.array([0.0,0.0])
            
            self.prev_pos = self.pos.copy()
            self.vel += self.acc
            self.vel = self.clamp(self.vel, self.speed_limit)
            self.pos += self.vel 
            self.acc *= 0

            r = 128 + int((255 / self.speed_limit) * self.vel[0])
            g = 128 + int((255 / self.speed_limit) * self.vel[1])
            b = 255
            o = 255 - int((self.lifespan / self.age) * 255)
            color = [ r, g, b, o]
            dpg.configure_item(self.p, p1=self.pos, p2=self.prev_pos, color=color)
            
        
            # Warp around the edges if the particle has gone out of bounds
            self.pos[0] = (self.pos[0] % self.horz_limit)
            self.pos[1] = (self.pos[1] % self.vert_limit)

    def apply_force(self, force):
        # give particles a bit of inertia for smoother lines
        self.acc += force/self.mass
        # if the force applying is in the opposite direction
        # kill the particle!
        if self.vel.dot(force) < 0:
            self.lifespan = 0

    def clamp(self, v, n_max):
        n = np.linalg.norm(v)
        if n > n_max:
            v *= (n_max / n)
        return v