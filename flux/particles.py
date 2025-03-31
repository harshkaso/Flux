import dearcygui as dcg
import numpy as np
from types import SimpleNamespace
from color_function_library import particle_color_function_registry
from config import UIDimensions, Properties, Colors, Defaults


class Particles:
    def __init__(self, context):
        self.context = context

        self.total_particles = Properties.total_particles
        self.speed = Properties.speed
        self.min_age = Properties.min_age
        self.max_age = Properties.max_age
        self.radius = Properties.radius
        self.angles = None

        self.colors = np.ndarray((4, self.total_particles.max_value))

        self.all_particles = np.ndarray((11, self.total_particles.max_value), dtype=object)

        self.color_function_list = particle_color_function_registry
        self._set_color_function(Defaults.particle_color_function)
    def setup_color_settings(self):
        self.function_combo = dcg.Combo(self.context, 
                                        width=UIDimensions.side_panel_width/2 ,
                                        items=list(self.color_function_list.keys()),
                                        label='Color Function',
                                        value=Defaults.particle_color_function,
                                        callback=lambda _0, _1, function_name: self._set_color_function(function_name))
        
        self.particle_alpha = dcg.Slider(self.context,
                                                   width=UIDimensions.side_panel_width/2,
                                                   format="int",
                                                   label="Alpha", 
                                                   value=Colors.particle_alpha,
                                                   min_value=0, 
                                                   max_value=255,
                                                   callback=self._set_particle_alpha)
        
        self.color_1_picker = dcg.ColorPicker(self.context,
                                                       width=UIDimensions.side_panel_width/2,
                                                       value=Colors.particle_color_1, 
                                                       label="Color 1",
                                                       picker_mode="wheel",
                                                       no_alpha=True,
                                                       callback=self._set_color)
        
        self.color_2_picker = dcg.ColorPicker(self.context,
                                                       width=UIDimensions.side_panel_width/2,
                                                       value=Colors.particle_color_2, 
                                                       label="Color 2",
                                                       picker_mode="wheel",
                                                       no_alpha=True,
                                                       callback=self._set_color)
        
        self.color_3_picker = dcg.ColorPicker(self.context,
                                                       width=UIDimensions.side_panel_width/2,
                                                       value=Colors.particle_color_3, 
                                                       label="Color 3",
                                                       picker_mode="wheel",
                                                       no_alpha=True,
                                                       callback=self._set_color)
    def _set_color_function(self, function_name):
        self.color_function = self.color_function_list[function_name]

    def _set_particle_alpha(self, _sender, _target, alpha):
        Colors.particle_alpha = alpha
    
    def _set_color(self, sender, _target, rgb_int):
        red   = rgb_int & 255
        green = (rgb_int >> 8) & 255
        blue  = (rgb_int >> 16) & 255
        if sender == self.color_1_picker:
            Colors.particle_color_1 = [red, green, blue]
        elif sender == self.color_2_picker:
            Colors.particle_color_2 = [red, green, blue]
        else:       
            Colors.particle_color_3 = [red, green, blue]       

    def setup_property_controls(self):
        self.total_particles_slider = dcg.Slider(self.context,
                width=UIDimensions.side_panel_width/2, 
                format="int",
                label="Total Particles",
                value=self.total_particles.value,
                min_value=self.total_particles.min_value,
                max_value=self.total_particles.max_value,
                callback=self._set_total_particles)
        
        self.speed_slider = dcg.Slider(self.context,
                width=UIDimensions.side_panel_width/2, 
                format="float",
                label="Speed",
                value=self.speed.value,
                min_value=self.speed.min_value,
                max_value=self.speed.max_value,
                callback=self._set_speed)
        
        self.min_age_slider = dcg.Slider(self.context,
                width=UIDimensions.side_panel_width/2, 
                format="int",
                label="Min Age",
                value=self.min_age.value,
                min_value=self.min_age.min_value,
                max_value=self.min_age.max_value,
                callback=self._set_min_age)
        
        self.max_age_slider = dcg.Slider(self.context,
                width=UIDimensions.side_panel_width/2, 
                format="int",
                label="Max Age",
                value=self.max_age.value,
                min_value=self.max_age.min_value,
                max_value=self.max_age.max_value,
                callback=self._set_max_age)
        
        self.random_radius_checkbox = dcg.Checkbox(self.context,
                label="Random Radius",
                value=self.radius.is_random,
                callback=self._set_radius_type)
        
        self.radius_slider = dcg.Slider(self.context,
                width=UIDimensions.side_panel_width/2, 
                format="float",
                label="Radius",
                value=self.radius.value,
                min_value=self.radius.min_value,
                max_value=self.radius.max_value,
                callback=self._set_radius)
       
    def _set_total_particles(self, sender, target, data):
        if data > self.total_particles.value:
            for particle in self.all_particles[10, self.total_particles.value:min(data + 1, self.total_particles.max_value)]:
                particle.show = True
        else:
            for particle in self.all_particles[10, data:self.total_particles.value]:
                particle.show = False
        self.total_particles.value = data

    def _set_speed(self, sender, target, speed):
        self.speed.value = speed

    def _set_min_age(self, sender, target, age):
        self.min_age.value = min(age, self.max_age.value-1)
        self.min_age_slider.value = self.min_age.value

    def _set_max_age(self, sender, target, age):
        self.max_age.value = max(age, self.min_age.value+1)
        self.max_age_slider.value = self.max_age.value

    def _set_radius_type(self, sender, target, is_random):
        self.radius.is_random = is_random
        self._update_particles_radius()

    def _set_radius(self, sender, target, radius):
        self.radius.value = radius
        self._update_particles_radius()
    
    def _update_particles_radius(self):
        if self.radius.is_random:
            self.all_particles[9] = np.random.rand(self.total_particles.max_value)*self.radius.value
        else:
            self.all_particles[9] = np.repeat(self.radius.value, self.total_particles.max_value)    
  
    def spawn(self):
        self.all_particles[0] = np.random.randint(UIDimensions.flowfield_width, size=self.total_particles.max_value)  # X
        self.all_particles[1] = np.random.randint(UIDimensions.flowfield_height, size=self.total_particles.max_value) # Y
        self.all_particles[2] = np.zeros(shape=self.total_particles.max_value) # Velocity_X
        self.all_particles[3] = np.zeros(shape=self.total_particles.max_value) # Velocity_Y
        self.all_particles[4] = np.random.randint(self.min_age.value, self.max_age.value, size=self.total_particles.max_value) # Age
        self.all_particles[5] = np.repeat(Colors.bg_color[0], self.total_particles.max_value) # Red
        self.all_particles[6] = np.repeat(Colors.bg_color[1], self.total_particles.max_value) # Green
        self.all_particles[7] = np.repeat(Colors.bg_color[2], self.total_particles.max_value) # Blue
        self.all_particles[8] = np.repeat(Colors.particle_alpha, self.total_particles.max_value) # Opacity
        self.all_particles[9] = np.repeat(self.radius.value, self.total_particles.max_value) # Radius
        # Draw particles
        for p in self.all_particles.T:
            p[10] = dcg.DrawCircle(self.context, center=(p[0], p[1]), radius=p[9], parent=self.context.flowfield_window.draw_area, fill=p[5:8], color=p[5:8], show=False)

    def apply_forces(self):
        # TODO: provide user control for damper
        force_x, force_y = np.cos(self.angles), np.sin(self.angles)
        # self.all_particles[2] = self.all_particles[2] + (self.angles[0] / (self.all_particles[9] + damper)) 
        # self.all_particles[3] = self.all_particles[3] + (self.angles[1] / (self.all_particles[9] + damper))
        self.all_particles[2] = self.all_particles[2] + (force_x / (self.all_particles[9]+1e-10))
        self.all_particles[3] = self.all_particles[3] + (force_y / (self.all_particles[9]+1e-10))
        self.all_particles[2], self.all_particles[3] = self.clamp_velocity(self.all_particles[2], self.all_particles[3], self.speed.value)

        self.all_particles[0] = self.all_particles[0] + self.all_particles[2]
        self.all_particles[1] = self.all_particles[1] + self.all_particles[3]
        


    def clamp_velocity(self, velocities_x, velocities_y, max_magnitude):
        velocities_x = np.array(velocities_x, dtype=float)
        velocities_y = np.array(velocities_y, dtype=float)
        magnitudes = np.sqrt(velocities_x**2 + velocities_y**2)
        clamped_magnitudes = np.minimum(magnitudes, max_magnitude)
        scale_factors = clamped_magnitudes / (magnitudes + 1e-10)  # Add a small value to avoid division by zero
        clamped_velocities_x = velocities_x * scale_factors
        clamped_velocities_y = velocities_y * scale_factors
        return clamped_velocities_x, clamped_velocities_y
      

    def get_invalid_indices(self):
        out_of_bounds = (self.all_particles[0] < 0) | (self.all_particles[0] > UIDimensions.flowfield_width) | (self.all_particles[1] < 0) | (self.all_particles[1] > UIDimensions.flowfield_height)
        expired = self.all_particles[4] <= 0
        return np.logical_or(out_of_bounds, expired)

    def reset_invalid_particles(self, invalid_indices, spawn_coordinates, masked_coordinates):
        total_invalid_particles = np.sum(invalid_indices)
        # mask the spawn locations
        masked_spawn_coordinates = np.argwhere(np.logical_and(spawn_coordinates,masked_coordinates)==1)
        if not (total_invalid_particles and len(masked_spawn_coordinates)):
            return
        spawn_indices = np.random.choice(len(masked_spawn_coordinates), size=total_invalid_particles)
        # self.all_particles[0, invalid_indices] = np.random.randint(UIDimensions.flowfield_width, size=total_invalid_particles)
        # self.all_particles[1, invalid_indices] = np.random.randint(UIDimensions.flowfield_height, size=total_invalid_particles)
        self.all_particles[:2, invalid_indices] = masked_spawn_coordinates[spawn_indices][:, ::-1].T
        self.all_particles[2, invalid_indices] = np.zeros(shape=total_invalid_particles)     
        self.all_particles[3, invalid_indices] = np.zeros(shape=total_invalid_particles)
        self.all_particles[4, invalid_indices] = np.random.randint(self.min_age.value,self.max_age.value + 1, size=total_invalid_particles)
        self.all_particles[5, invalid_indices] = np.repeat(Colors.bg_color[0], total_invalid_particles)
        self.all_particles[6, invalid_indices] = np.repeat(Colors.bg_color[1], total_invalid_particles)
        self.all_particles[7, invalid_indices] = np.repeat(Colors.bg_color[2], total_invalid_particles)
        for particle in self.all_particles[10, invalid_indices]:
            particle.show = False

    def update_colors(self, color_context, color_1, color_2, color_3, base_aplha):
        self.all_particles[5:9] = self.color_function.get_colors(color_context, color_1, color_2, color_3, base_aplha)

    def senesce(self, masked_indices, fade = 1):
        total_masked_particles = np.sum(masked_indices)
        if total_masked_particles:
            self.all_particles[4, masked_indices] = np.random.choice(fade, total_masked_particles)
        self.all_particles[4] -= 1

    def update(self):
        for particle in self.all_particles[:,:self.total_particles.value].T:
            particle[10].fill = particle[5:9]
            particle[10].color = particle[5:9]
            particle[10].center = particle[0:2] # Location (X, Y)
            particle[10].radius = particle[9] # Radius
            particle[10].show = True