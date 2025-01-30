from types import SimpleNamespace
import dearpygui.dearpygui as dpg
import numpy as np
import globals


class Particles:
    def __init__(self):
        pass
        
    def setup_controls(self):
        dpg.add_slider_int(width=globals.UIDimensions.side_panel_width/2, 
                           label='particles', 
                           tag=globals.UITags.total_particles,
                           default_value=globals.ParticleVariables.total_particles.value, 
                           min_value=globals.ParticleVariables.total_particles.min_value, 
                           max_value=globals.ParticleVariables.total_particles.max_value, 
                           callback=self.set_particle_variable)
        dpg.add_slider_float(width=globals.UIDimensions.side_panel_width/2, 
                             label='speed',
                             default_value=globals.ParticleVariables.speed.value, 
                             min_value=globals.ParticleVariables.speed.min_value, 
                             max_value=globals.ParticleVariables.speed.max_value, 
                             callback=self.set_particle_variable)
        dpg.add_slider_int(width=globals.UIDimensions.side_panel_width/2, 
                           label='min age', 
                           tag=globals.UITags.min_age, 
                           default_value=globals.ParticleVariables.min_age.value,
                           min_value=globals.ParticleVariables.min_age.min_value, 
                           max_value=globals.ParticleVariables.min_age.max_value,
                           callback=self.set_particle_variable)
        dpg.add_slider_int(width=globals.UIDimensions.side_panel_width/2, 
                           label='max age', 
                           tag=globals.UITags.max_age,
                           default_value=globals.ParticleVariables.max_age.value, 
                           min_value=globals.ParticleVariables.max_age.min_value,
                           max_value=globals.ParticleVariables.max_age.max_value,
                           callback=self.set_particle_variable)
        dpg.add_checkbox(label='random radius',
                         tag=globals.UITags.random_radius,
                         default_value=globals.ParticleVariables.random_radius,
                         callback=self.set_particle_variable)
        dpg.add_slider_float(width=globals.UIDimensions.side_panel_width/2,
                             label='radius',
                             tag=globals.UITags.radius,
                             default_value=globals.ParticleVariables.radius.value,
                             min_value=globals.ParticleVariables.radius.min_value,
                             max_value=globals.ParticleVariables.radius.max_value,
                             callback=self.set_particle_variable)
    
    def set_particle_variable(self, sender, data):
        if sender == globals.UITags.total_particles:
            globals.ParticleVariables.total_particles.value = data
            # TODO: update total particles in the system
        elif sender == globals.UITags.speed:
            globals.ParticleVariables.speed.value = data
        elif sender == globals.UITags.min_age:
            globals.ParticleVariables.min_age.value = data
        elif sender == globals.UITags.max_age:
            globals.ParticleVariables.max_age.value = data
        elif sender == globals.UITags.random_radius:
            globals.ParticleVariables.random_radius = data
            # TODO: update radius of particles to be random
        elif sender == globals.UITags.radius:
            globals.ParticleVariables.radius.value = data
            # TODO: update radius of particles