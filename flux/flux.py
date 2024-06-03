import dearpygui.dearpygui as dpg
import numpy as np
import color_functions as cf
import flowfield_functions as fff
import config as cfg

def spawn_paricles():
  cfg.particles[0] = [np.random.random() * cfg.ff_width for _ in range(cfg.cc_size)]  # X
  cfg.particles[1] = [np.random.random() * cfg.ff_height for _ in range(cfg.cc_size)] # Y
  cfg.particles[2] = [np.random.randint(cfg.min_age, cfg.max_age) for _ in range(cfg.cc_size)] # age
  cfg.particles[3] = np.repeat(cfg.bg_color[0], cfg.cc_size) # Red
  cfg.particles[4] = np.repeat(cfg.bg_color[1], cfg.cc_size) # Green
  cfg.particles[5] = np.repeat(cfg.bg_color[2], cfg.cc_size) # Blue
  cfg.particles[6] = np.repeat(cfg.p_alpha, cfg.cc_size) # Opacity
  # for each coordinates draw a particle
  for p in cfg.particles.T:
    p[7] = dpg.draw_circle(center=(p[0], p[1]), radius=1, parent='flowfield', fill=list(p[3:7]), color=list(p[3:7]), show=False) # Reference to drawn object

def recalc_particles():
  cfg.coords[0] = cfg.particles[0]
  cfg.coords[1] = cfg.particles[1]
  cfg.coords[2] = np.repeat(dpg.get_frame_count(), cfg.cc_size)

  dx, dy = cfg.ff_func(cfg.coords)
  
  cfg.particles[0] = np.add(cfg.particles[0], np.multiply(dx, cfg.speed))
  cfg.particles[1] = np.add(cfg.particles[1], np.multiply(dy, cfg.speed))
  cfg.particles[2] = np.add(cfg.particles[2], -1)

  # Reset particles if out of bounds or expired
  out_of_bounds = (cfg.particles[0] < 0) | (cfg.particles[0] > cfg.ff_width) | (cfg.particles[1] < 0) | (cfg.particles[1] > cfg.ff_height)
  expired = cfg.particles[2] <= 0
  reset_indices = np.logical_or(out_of_bounds, expired)
  cfg.particles[0, reset_indices] = np.multiply(np.random.rand(np.sum(reset_indices)), cfg.ff_width)
  cfg.particles[1, reset_indices] = np.multiply(np.random.rand(np.sum(reset_indices)), cfg.ff_height)
  cfg.particles[2, reset_indices] = np.random.randint(cfg.min_age, cfg.max_age + 1, size=np.sum(reset_indices))

  args = {
    'particles': cfg.particles,
    'dx': dx,
    'dy': dy,
    'max_particles': cfg.max_particles,
    'ttl_particles': cfg.ttl_particles,
    'ff_width': cfg.ff_width,
    'ff_height': cfg.ff_height,
    'speed': cfg.speed,
    'min_age': cfg.min_age,
    'max_age': cfg.max_age,
  }
  cfg.particles[3:7] = cfg.clr_func(cfg.min_rgb, cfg.max_rgb, cfg.p_alpha, args) # RGB

  for p in cfg.particles[:,:cfg.ttl_particles].T:
    clr = list(p[3:7])
    dpg.configure_item(int(p[7]), center=(p[0], p[1]), fill=clr, color=clr, show=True)

def background(clr):
  with dpg.mutex():
    # Window Background
    if dpg.does_item_exist('w_background'):
      dpg.configure_item('w_background', fill=clr, color=clr,pmax=(cfg.ff_width, cfg.ff_height), show=True)
    else:
      dpg.draw_rectangle(tag='w_background', pmin=(0,0), pmax=(cfg.ff_width, cfg.ff_height), parent='flowfield', fill=clr, color=clr)
      
def dimmer(clr, d_alpha):
  with dpg.mutex():
    # Dimmer
    # Let the dimmer be drawn every frame
    color = clr[:3]
    color.append(cfg.d_alpha)
    if dpg.does_item_exist('dimmer'):
        dpg.configure_item('dimmer', pmax=(cfg.ff_width, cfg.ff_height), fill=color, color=color)
    else:
      dpg.draw_rectangle(tag='dimmer', pmin=(0,0), pmax=(cfg.ff_width, cfg.ff_height), parent='flowfield', fill=color, color=color)

def handle_viewport_resize(sender, data):
  with dpg.mutex():
    if data[2] != cfg.w_width or data[3] != cfg.w_height:
      cfg.w_width, cfg.w_height = data[2:]
      cfg.ff_width = cfg.w_width - cfg.sp_width
      cfg.ff_height = cfg.w_height
      dpg.configure_item('parameters', pos=(cfg.ff_width, 0)) # Update side panel position
      background(cfg.bg_color)
      dimmer(cfg.bg_color, cfg.d_alpha)
      dpg.set_frame_callback(dpg.get_frame_count()+1, callback=lambda: dpg.output_frame_buffer(callback=init_frame_buffer))

  
def init_frame_buffer(sender, buffer):
  # Prepare for frame buffer handling
  with dpg.mutex():
    # Setup Initial Frame
    with dpg.texture_registry():
      if dpg.does_item_exist(cfg.prev_frame_texture):
        dpg.delete_item(cfg.prev_frame_texture)
      cfg.prev_frame_texture = dpg.add_raw_texture(width=cfg.w_width, height=cfg.w_height, default_value=buffer, format=dpg.mvFormat_Float_rgba)
    if dpg.does_item_exist(cfg.prev_frame):
      dpg.delete_item(cfg.prev_frame)
    cfg.prev_frame = dpg.add_image(cfg.prev_frame_texture, width=cfg.ff_width, height=cfg.ff_height, parent='flowfield', pos=(0,0), uv_min=(0,0), uv_max=(cfg.ff_width/cfg.w_width, 1))
    # Start the frame buffer
    
    dpg.set_frame_callback(dpg.get_frame_count()+1, callback=lambda: dpg.output_frame_buffer(callback=clear_frame))

def clear_frame(sender, buffer):
  with dpg.mutex():
    if dpg.is_item_shown(cfg.prev_frame):
      dpg.hide_item(cfg.prev_frame)
      dpg.set_frame_callback(dpg.get_frame_count()+1, callback=lambda: dpg.output_frame_buffer(callback=clear_frame))
    else:
      dpg.set_value(cfg.prev_frame, buffer)
      dpg.show_item(cfg.prev_frame)
      # Make sure the background is only drawn once
      if dpg.is_item_shown('w_background'):
        dpg.hide_item('w_background')
      dpg.set_frame_callback(dpg.get_frame_count()+1, callback=lambda: dpg.output_frame_buffer(callback=handle_frame_buffer))

def handle_frame_buffer(sender, buffer):
  with dpg.mutex():
    dpg.set_value(cfg.prev_frame_texture, buffer)
    recalc_particles()
    dpg.set_frame_callback(dpg.get_frame_count()+3, callback=lambda: dpg.output_frame_buffer(callback=handle_frame_buffer))

def setup_flux():
  # Callbacks
  def set_flowfield_function(sender, data):
    dpg.delete_item(cfg.ff_func_settings, children_only=True)
    cfg.ff_func = fff.get_flowfield_function(data)

  def set_ttl_particles(sender, data):
    if data > cfg.ttl_particles:
      for p in cfg.particles[7,cfg.ttl_particles:min(data+1, cfg.max_particles)]:
        dpg.configure_item(int(p), show=True)
    else:
      for p in cfg.particles[7, data:cfg.ttl_particles]:
        dpg.configure_item(int(p), show=False)
    cfg.ttl_particles = data

  def set_particle_speed(sender, data):
    cfg.speed = data

  def set_color_function(sender, data):
    cfg.clr_func = cf.get_color_function(data)

  def set_min_max_age(sender, data):
    if sender == 'min-age':
      cfg.min_age = data
    elif sender == 'max-age':
      cfg.max_age = data

  def set_min_max_rgb(sender, data):
    if sender == 'min_rgb':
      cfg.min_rgb = [int(c*255) for c in data]
    elif sender == 'max_rgb':
      cfg.max_rgb = [int(c*255) for c in data]

  def set_particle_opacity(sender, data):
    cfg.p_alpha = data
  
  def set_dimmer_opacity(semder, data):
    cfg.d_alpha = data
    background(cfg.bg_color)
    dimmer(cfg.bg_color, cfg.d_alpha)
    dpg.set_frame_callback(dpg.get_frame_count()+1, callback=lambda: dpg.output_frame_buffer(callback=clear_frame))


  def set_background_color(sender, data):
    r,g,b,a = [int(c*255) for c in data]
    cfg.bg_color = [r,g,b,a]
    background(cfg.bg_color)
    dimmer(cfg.bg_color, cfg.d_alpha)
    # Calculate Luminance of background
    # Needed for runntime UI themes.
    l = 0.2126 * r + 0.7152 * g + 0.0722 * b
    threshold = 180
    a = 180
    with dpg.theme() as flowfield_theme:
      with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, [r,g,b,a], category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, [255,255,255,255] if l < threshold else [0,0,0,255], category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, [int(r-(r/20)),int(g-(g/20)),int(b-(b/20)),100], category=dpg.mvThemeCat_Core)
    dpg.bind_item_theme('flowfield', flowfield_theme)    
    dpg.set_frame_callback(dpg.get_frame_count()+1, callback=lambda: dpg.output_frame_buffer(callback=clear_frame))
      
  def handle_dropdown(sender, data, group):
    if dpg.is_item_shown(group):
      dpg.configure_item(sender, direction=dpg.mvDir_Right)
      dpg.configure_item(group, show=False)
    else:
      dpg.configure_item(sender, direction=dpg.mvDir_Down)
      dpg.configure_item(group, show=True)

  # Main Window
  with dpg.window(tag='flowfield', pos=(0,0)):
    # Theme setting
    dpg.set_primary_window('flowfield', True)
    with dpg.theme() as flowfield_theme:
      with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, cfg.bg_color, category=dpg.mvThemeCat_Core)
    dpg.bind_item_theme('flowfield', flowfield_theme)

    # Flux GUI
    with dpg.child_window(tag='parameters', pos=(cfg.ff_width, 0), width=cfg.sp_width, height=-1):
      with dpg.theme() as side_panel_theme:
        with dpg.theme_component(dpg.mvAll):
          dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8)
      dpg.bind_item_theme('parameters', side_panel_theme)
      
      # Flowfield Settings UI
      dpg.add_spacer(height=3)
      with dpg.group(horizontal=True):
        dpg.add_button(tag='ff-dropdown', arrow=True, direction=dpg.mvDir_Down, callback=handle_dropdown, user_data='flowfield-settings')
        dpg.add_text(default_value='Flowfield Properties')
      with dpg.group(tag='flowfield-settings'):
        dpg.add_combo(width=cfg.sp_width/2, label='FlowField Function', tag='flowfield-functions', items=fff.get_flowfield_function_names(), default_value=cfg.default_fff, callback=set_flowfield_function)
      with dpg.group(tag=cfg.ff_func_settings):
        # UI container for selected Flowfield Function.
        pass
      dpg.add_separator()
      
      # Particle Settings UI
      with dpg.group(horizontal=True):
        dpg.add_button(tag='pp-dropdown', arrow=True, direction=dpg.mvDir_Down, callback=handle_dropdown, user_data='particle-settings')
        dpg.add_text(default_value='Particle Properties')
      with dpg.group(tag='particle-settings'):
        dpg.add_slider_int(width=cfg.sp_width/2, label='particles', tag='total-cfg.particles', min_value=0, default_value=cfg.ttl_particles, max_value=cfg.max_particles, callback=set_ttl_particles)
        dpg.add_slider_float(width=cfg.sp_width/2, label='speed', min_value=0.5, default_value=cfg.speed, max_value=4, callback=set_particle_speed)
        dpg.add_slider_int(width=cfg.sp_width/2, label='min age', tag='min-age', min_value=cfg.min_age, default_value=cfg.min_age, max_value=100, callback=set_min_max_age)
        dpg.add_slider_int(width=cfg.sp_width/2, label='max age', tag='max-age', min_value=101, default_value=cfg.max_age, max_value=cfg.max_age, callback=set_min_max_age)
    
      dpg.add_separator()

      # Color Settings UI
      with dpg.group(horizontal=True):
        dpg.add_button(tag='cl-dropdown', arrow=True, direction=dpg.mvDir_Down, callback=handle_dropdown, user_data='color-settings')
        dpg.add_text(default_value='Color Settings')
      with dpg.group(tag='color-settings'):
        dpg.add_combo(width=cfg.sp_width/2, label='Color Function', tag='color-functions', items=cf.get_color_function_names(), default_value=cfg.default_cf, callback=set_color_function)
        with dpg.tab_bar(tag='color-pickers'):
          with dpg.tab(tag='background', label='background'):
            dpg.add_slider_int(width=cfg.sp_width/2, label='dimmer alpha', default_value=cfg.d_alpha, max_value=255, callback=set_dimmer_opacity)
            dpg.add_color_picker(width=cfg.sp_width/2, label='background', tag='bg_rgb', default_value=cfg.bg_color, no_tooltip=True, no_alpha=True, callback=set_background_color)
          with dpg.tab(tag='particles', label='particles'):
            dpg.add_slider_int(width=cfg.sp_width/2, label='particle alpha', default_value=cfg.p_alpha, max_value=255, callback=set_particle_opacity)
            dpg.add_color_picker(width=cfg.sp_width/2, label='min_rgb', tag='min_rgb', default_value=cfg.min_rgb, no_tooltip=True, no_alpha=True, callback=set_min_max_rgb)
            dpg.add_color_picker(width=cfg.sp_width/2, label='max_rgb', tag='max_rgb', default_value=cfg.max_rgb, no_tooltip=True, no_alpha=True, callback=set_min_max_rgb)
      # Bottom Padding
      dpg.add_spacer(height=3)

  # initializing with default functions
  spawn_paricles()
  cfg.ff_func = fff.get_flowfield_function(cfg.default_fff)   # FlowField Function
  cfg.clr_func = cf.get_color_function(cfg.default_cf)    # Color Function


  
def start_flux():
  # Start Flux
  dpg.create_context()
  dpg.create_viewport(title='Flux', width=cfg.w_width, height=cfg.w_height)
  dpg.setup_dearpygui()
  setup_flux()
  dpg.show_viewport()
  dpg.set_viewport_resize_callback(callback=handle_viewport_resize)
  # dpg.set_frame_callback(20, callback=lambda: dpg.output_frame_buffer(callback=init_frame_buffer))
  # dpg.set_viewport_vsync(False)
  # dpg.show_metrics()
  # dpg.show_style_editor()
  dpg.start_dearpygui()
  dpg.destroy_context()
