# Restructured entire project to have more scalability and clarity
# However, somehow I ended up just as lost as I was before
# Screw it, this is a frankenstein of a code, Im over it.

try:
    from __init__ import __version__
    from config import UIDimensions, Colors
    from stylemanager import StyleManager
    from particles import Particles
    from flowfield import Flowfield
except ImportError as e:
    raise ImportError(f"{str(e)}")

# import dearpygui.dearpygui as dpg
import dearcygui as dcg
import numpy as np
from types import SimpleNamespace


class FluxApp(dcg.Context):
    def __init__(self, **kwargs):
        # Create the dearpygui context
        super().__init__()
        self.style_manager = StyleManager(self)

        
        self.viewport.initialize(title=f'Flux - {__version__}', width=UIDimensions.viewport_width, height=UIDimensions.viewport_height, min_width=UIDimensions.viewport_width, min_height=UIDimensions.viewport_height, resize_callback=self._handle_viewport_resize)
        self.viewport.retrieve_framebuffer = True
        self.viewport.vsync = False
        with dcg.Window(self, primary=True, no_move=True, font=self.style_manager.regular_font):
            with dcg.HorizontalLayout(self, theme=self.style_manager.app_layout_theme):
                # Main Window
                self.flowfield_window = FlowFeildWindow(self, width=UIDimensions.flowfield_width, height=-1, theme=self.style_manager.flowfield_window_theme)
                self.particles = Particles(self)
                self.flowfield = Flowfield(self)
                
                self.color_context = SimpleNamespace(
                    particles = self.particles,
                    flowfield = self.flowfield
                )
                self.particles.spawn()
                
                # Side Panel
                self.side_panel = SidePanel(self, width=UIDimensions.side_panel_width, height=-1, theme=self.style_manager.side_panel_theme)
            
    def _handle_viewport_resize(self, sender, viewport: dcg.Viewport):
        # Update viewport dimensions
        UIDimensions.viewport_width = viewport.width
        UIDimensions.viewport_height = viewport.height
        # Calculate the new dimensions for the flowfield window
        UIDimensions.flowfield_width = UIDimensions.viewport_width - UIDimensions.side_panel_width
        UIDimensions.flowfield_height = UIDimensions.viewport_height
        # Update the dimensions of the flowfield window
        self.flowfield_window.width = UIDimensions.flowfield_width
        self.flowfield_window.height = UIDimensions.flowfield_height
        self.flowfield_window.resize_frame()
        self.flowfield.handle_window_resize()
        
    def run(self):
        try:

            while self.running:
                self.viewport.render_frame()
                self.frame_count = self.viewport.metrics['frame_count']

                self.flowfield_window.depth_layer(color=Colors.bg_color, alpha=Colors.depth_layer_alpha)
                self.flowfield_window.render_previous_frame(self.viewport.framebuffer)

                self.particles.angles = self.flowfield.function.get_angles(self.particles.all_particles, self.frame_count)
                self.particles.apply_forces()
                invalid_indices = self.particles.get_invalid_indices()
                self.particles.reset_invalid_particles(invalid_indices, self.flowfield.function.spawn_coordinates, self.flowfield.mask.masked_coordinates)
                masked_indices = self.flowfield.mask.masked_coordinates[self.particles.all_particles[1].astype(int),self.particles.all_particles[0].astype(int)] != 1
                self.particles.senesce(masked_indices, self.flowfield.mask_fade.value)
                self.particles.update_colors(self.color_context, Colors.particle_color_1, Colors.particle_color_2, Colors.particle_color_3, Colors.particle_alpha)
                self.particles.update()

                self.delta_whole_frame = self.viewport.metrics['delta_whole_frame']
                self.fps = 1/self.delta_whole_frame
                # self.side_panel.fps.value = self.viewport.metrics['delta_whole_frame']
                self.side_panel.fps.value = self.fps
        except Exception as e:
            print(e)
            print(
        type(e).__name__,          # TypeError
        __file__,                  # /tmp/example.py
        e.__traceback__.tb_lineno  # 2
    )

            # print(e.__traceback__)

class FlowFeildWindow(dcg.ChildWindow):
    def __init__(self, context, **kwargs):
        super().__init__(context, **kwargs)
        self.width  = UIDimensions.flowfield_width
        self.height = UIDimensions.flowfield_height
        self.skip_frame = False
        with self:
            self.prev_frame = dcg.Image(context,width=self.width, height=self.height, uv=[0,1,self.width/UIDimensions.viewport_width, 0])
            with dcg.DrawInWindow(context, width=-1, height=-1, pos_to_parent=(0,0)) as self.canvas:
                # self.prev_frame = dcg.Image(context, width=UIDimensions.flowfield_width, height=UIDimensions.flowfield_height, uv=[0.,0.,UIDimensions.flowfield_width/UIDimensions.viewport_width, 1.])
                
                self.dimmer = dcg.DrawRect(self.context, pmin=(0,0), pmax=(self.width, self.height), fill=Colors.bg_color+[Colors.depth_layer_alpha], color=Colors.bg_color+[Colors.depth_layer_alpha])
                with dcg.DrawingList(context) as self.draw_area:
                    pass

    def depth_layer(self, color, alpha):
        bg_color = color + [alpha]
        self.dimmer.fill = bg_color
        self.dimmer.color = bg_color
    
    def setup_background_controls(self):
        self.depth_layer_alpha_slider = dcg.Slider(self.context,
                                                   width=UIDimensions.side_panel_width/2,
                                                   format="int",
                                                   label="Alpha", 
                                                   value=Colors.depth_layer_alpha,
                                                   min_value=0, 
                                                   max_value=255,
                                                   callback=self._set_depth_layer_alpha)
        
        self.background_color_picker = dcg.ColorPicker(self.context,
                                                       width=UIDimensions.side_panel_width/2,
                                                       value=Colors.bg_color, 
                                                       label="Color",
                                                       picker_mode="wheel",
                                                       no_alpha=True,
                                                       callback=self._set_background_color)
    
    def _set_depth_layer_alpha(self, sender, target, alpha):
        Colors.depth_layer_alpha = alpha

    def _set_background_color(self, sender, target, rgb_int):
        red   = rgb_int & 255
        green = (rgb_int >> 8) & 255
        blue  = (rgb_int >> 16) & 255
        Colors.bg_color = [red, green, blue]
        self.context.style_manager.update_flowfield_window_theme(Colors.bg_color)
        self.skip_frame = True

    def resize_frame(self):
        self.prev_frame.width = self.width
        self.prev_frame.height = self.height
        self.prev_frame.uv = [0,1,self.width/UIDimensions.viewport_width, 0]
        self.dimmer.pmax = (self.width, self.height)
        self.skip_frame = True


    def render_previous_frame(self, previous_frame: dcg.Texture):
        self.prev_frame.texture = previous_frame
        self.prev_frame.show = not self.skip_frame
        self.skip_frame = False
        
    

class SidePanel(dcg.ChildWindow):
    def __init__(self, context, **kwargs):
        super().__init__(context, **kwargs)
        with self:
            with dcg.HorizontalLayout(context, theme=context.style_manager.dropdown_btn_theme):
                dcg.Button(context, arrow=True, direction=dcg.ButtonDirection.DOWN, callback=lambda sender, _: self._handle_dropdown(sender, self.flowfield_settings))
                dcg.Text(context, value="Flowfield Settings", font=context.style_manager.bold_font)
            with dcg.VerticalLayout(context, theme=context.style_manager.properties_theme) as self.flowfield_settings:
                context.flowfield.setup_controls()

            
            dcg.Separator(context)

            with dcg.HorizontalLayout(context, theme=context.style_manager.dropdown_btn_theme):
                dcg.Button(context, arrow=True, direction=dcg.ButtonDirection.DOWN, callback=lambda sender, _: self._handle_dropdown(sender, self.mask_settings))
                dcg.Text(context, value="Mask Settings", font=context.style_manager.bold_font)
            with dcg.VerticalLayout(context, theme=context.style_manager.properties_theme) as self.mask_settings:
                context.flowfield.setup_mask_controls()
                pass
            
            dcg.Separator(context)

            with dcg.HorizontalLayout(context, theme=context.style_manager.dropdown_btn_theme):
                dcg.Button(context, arrow=True, direction=dcg.ButtonDirection.DOWN, callback=lambda sender, _: self._handle_dropdown(sender, self.particle_settings))
                dcg.Text(context, value="Particle Settings", font=context.style_manager.bold_font)
            with dcg.VerticalLayout(context, theme=context.style_manager.properties_theme) as self.particle_settings:
                context.particles.setup_property_controls()
            
            dcg.Separator(context)

            with dcg.HorizontalLayout(context, theme=context.style_manager.dropdown_btn_theme):
                dcg.Button(context, arrow=True, direction=dcg.ButtonDirection.DOWN, callback=lambda sender, _: self._handle_dropdown(sender, self.color_settings))
                dcg.Text(context, value="Color Settings", font=context.style_manager.bold_font)
            with dcg.VerticalLayout(context, theme=context.style_manager.properties_theme) as self.color_settings:
                with dcg.TabBar(context, width=-1, theme=context.style_manager.tab_theme):
                    with dcg.Tab(context, label="Background"):
                        with dcg.VerticalLayout(context, theme=context.style_manager.properties_theme) as self.background_color_settings:
                            # Background Color settings
                            context.flowfield_window.setup_background_controls()
                        pass
                    with dcg.Tab(context, label="Particle"):
                        with dcg.VerticalLayout(context, theme=context.style_manager.properties_theme) as self.particle_color_settings:
                            # Particle Color Settings 
                            context.particles.setup_color_settings()
                            pass
            
            dcg.Separator(context)

            self.fps = dcg.Text(context)


    def _handle_dropdown(self, sender, target: dcg.uiItem):
        if sender.direction == dcg.ButtonDirection.DOWN:
            sender.direction = dcg.ButtonDirection.RIGHT
            target.show = False
        else:
            sender.direction = dcg.ButtonDirection.DOWN
            target.show = True