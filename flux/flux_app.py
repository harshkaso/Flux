try:
    from __init__ import __version__
    import globals
    from stylemanager import StyleManager
    from particles import Particles
except ImportError as e:
    raise ImportError(f"{str(e)}")

# import dearpygui.dearpygui as dpg
import dearcygui as dcg

class FluxApp:
    def __init__(self):
        # Create the dearpygui context
        self.context = dcg.Context()
        # self.particles = Particles()
        # self.style_manager = StyleManager()
        

    
    def run(self):
        # Viewport
        self.context.viewport.initialize(title=f'Flux - {__version__}', width=globals.UIDimensions.viewport_width, height=globals.UIDimensions.viewport_height)
        print(f'{self.context.viewport.width=}')
        with dcg.Window(self.context, primary=True):
            pass
        while self.context.running:
            self.context.viewport.render_frame()       
        # dpg.create_viewport(title=f'Flux - {__version__}', width=globals.UIDimensions.viewport_width, height=globals.UIDimensions.viewport_height,
        #  min_width=globals.UIDimensions.viewport_width, min_height=globals.UIDimensions.viewport_height)
        # # Main Window
        # with dpg.window(tag=globals.UITags.app_window, pos=(0,0)):
        #     dpg.set_primary_window(globals.UITags.app_window, True)
        #     dpg.add_draw_layer(tag=globals.UITags.particles_container)
            
        #     with dpg.child_window(tag=globals.UITags.side_panel, pos=(globals.UIDimensions.flowfield_width, 0), width=globals.UIDimensions.side_panel_width, height=-1):
        #         dpg.add_spacer(height=3)
        #         # TODO: Add dropdowns for each section
        #         with dpg.group(horizontal=True):
        #             dpg.add_button(tag='pp-dropdown', arrow=True, direction=dpg.mvDir_Down, callback=self._handle_dropdown, user_data=globals.UITags.particle_settings)
        #             dpg.add_text(default_value='Particle Properties')
        #         with dpg.group(tag=globals.UITags.particle_settings):
        #             self.particles.setup_controls()
                
        # self.style_manager.update_app_theme()
            
            

        # dpg.setup_dearpygui()
        # dpg.show_viewport()
        # dpg.show_metrics()
        # dpg.set_viewport_vsync(False)
        # # dpg.set_viewport_resize_callback(callback=handle_viewport_resize)
        # dpg.start_dearpygui()
        # dpg.destroy_context()
        
    def _handle_dropdown(self, sender, data, group):
        if dpg.is_item_shown(group):
            dpg.configure_item(sender, direction=dpg.mvDir_Right)
            dpg.configure_item(group, show=False)
        else:
            dpg.configure_item(sender, direction=dpg.mvDir_Down)
            dpg.configure_item(group, show=True)
