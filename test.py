# import dearpygui.dearpygui as dpg
# import numpy as np
# import time

# # Constants
# NUM_PARTICLES = 15000
# WIDTH, HEIGHT = 1200, 800
# SPEED = 0.5
# NOISE_SCALE = 0.005
# ACCELERATION = 0.2
# VELOCITY_DAMPING = 0.98

# # Initialize particles
# particles = np.zeros((NUM_PARTICLES, 4), dtype=np.float32)
# particles[:, 0] = np.random.uniform(0, WIDTH, NUM_PARTICLES)
# particles[:, 1] = np.random.uniform(0, HEIGHT, NUM_PARTICLES)

# def vector_field(x, y, t):
#     angle = (np.cos(x * NOISE_SCALE) + np.sin(y * NOISE_SCALE)) * 10
#     return np.cos(angle), np.sin(angle)

# def update_particles():
#     global particles
#     current_time = time.time() * SPEED
    
#     x = particles[:, 0]
#     y = particles[:, 1]
    
#     vx, vy = vector_field(x, y, current_time)
    
#     particles[:, 2] = particles[:, 2] * VELOCITY_DAMPING + vx * ACCELERATION
#     particles[:, 3] = particles[:, 3] * VELOCITY_DAMPING + vy * ACCELERATION
    
#     particles[:, 0] = (particles[:, 0] + particles[:, 2]) % WIDTH
#     particles[:, 1] = (particles[:, 1] + particles[:, 3]) % HEIGHT

# def render_callback():
#     global SPEED, NOISE_SCALE, ACCELERATION
#     SPEED = dpg.get_value("speed")
#     NOISE_SCALE = dpg.get_value("noise_scale")
#     ACCELERATION = dpg.get_value("accel")
    
#     update_particles()
#     dpg.set_value('plot_series', [particles[:, 0].tolist(), particles[:, 1].tolist()])

# dpg.create_context()

# with dpg.window(tag="Main Window"):
#     dpg.set_primary_window("Main Window", True)
#     with dpg.theme() as flowfield_theme:
#       with dpg.theme_component(dpg.mvAll):
#         dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
#     dpg.bind_item_theme("Main Window", flowfield_theme)

#     with dpg.plot(label="Flow Field", width=-1, height=-1, no_title=True, no_inputs=True, no_menus=True, no_frame=True):
#         x_axis = dpg.add_plot_axis(dpg.mvXAxis, no_gridlines=True, no_tick_labels=True, no_tick_marks=True)
#         y_axis = dpg.add_plot_axis(dpg.mvYAxis, no_gridlines=True, no_tick_labels=True, no_tick_marks=True)
        
#         # Universal parameter approach
#         dpg.add_scatter_series(
#             x=particles[:, 0].tolist(),
#             y=particles[:, 1].tolist(),
#             label="Particles",
#             parent=y_axis,
#             tag="plot_series",
#             # size=1,  # Direct size parameter
#             # outline=False  # Disable outline for better performance
#         )


# with dpg.window(label="Controls", pos=(10, 10)):
#     dpg.add_slider_float(label="Speed", tag="speed", default_value=SPEED, min_value=0.1, max_value=2.0)
#     dpg.add_slider_float(label="Noise Scale", tag="noise_scale", default_value=NOISE_SCALE, min_value=0.001, max_value=0.02)
#     dpg.add_slider_float(label="Acceleration", tag="accel", default_value=ACCELERATION, min_value=0.01, max_value=1.0)

# dpg.create_viewport(title='Flow Field Visualization', width=WIDTH, height=HEIGHT)
# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.set_viewport_vsync(False)
# dpg.show_metrics()
# dpg.set_primary_window("Main Window", True)

# # Main loop
# while dpg.is_dearpygui_running():
#     render_callback()
#     dpg.render_dearpygui_frame()

# dpg.destroy_context()

import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Set screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flowfield Visualization")

# --- Flowfield Functions ---

def create_flowfield(width, height, func_name, **kwargs):
    """Generates a flowfield based on the chosen function."""
    flowfield = np.zeros((width, height, 2))  # Store x, y components of vectors
    
    if func_name == "radial":
        center_x, center_y = kwargs.get("center_x", width // 2), kwargs.get("center_y", height // 2)
        for x in range(width):
            for y in range(height):
                dx = x - center_x
                dy = y - center_y
                magnitude = np.sqrt(dx**2 + dy**2)
                flowfield[x, y] = np.array([dx / magnitude, dy / magnitude]) 
    
    # Add more flowfield functions here...

    return flowfield

# --- Particle Class ---
class Particle:
    def __init__(self, x, y, color=(255, 255, 255)):
        self.position = np.array([x, y])
        self.velocity = np.array([0, 0])
        self.color = color
        self.lifespan = np.random.randint(100, 300)  # Random lifespan

    def update(self, flowfield):
        """Updates particle position based on flowfield."""
        x, y = int(self.position[0]), int(self.position[1])
        if 0 <= x < width and 0 <= y < height:
            self.velocity = flowfield[x, y]
            self.position += self.velocity
        else:
            self.position = np.random.rand(2) * np.array([width, height]) # Respawn

        self.lifespan -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position.astype(int), 5)

# --- Main Application Loop ---

# Flowfield settings
flowfield_func = "radial"
flowfield_params = {"center_x": width // 2, "center_y": height // 2}

# Particle settings
num_particles = 1000
particles = [Particle(*(np.random.rand(2) * np.array([width, height]))) for _ in range(num_particles)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update ---
    flowfield = create_flowfield(width, height, flowfield_func, **flowfield_params)
    for particle in particles:
        particle.update(flowfield)
        if particle.lifespan <= 0:  
            particle.position = np.random.rand(2) * np.array([width, height])
            particle.lifespan = np.random.randint(100, 300)

    # --- Draw ---
    screen.fill((0, 0, 0))  # Clear the screen

    for particle in particles:
        particle.draw(screen)

    pygame.display.flip()

pygame.quit()
