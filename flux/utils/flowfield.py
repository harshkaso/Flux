import dearpygui.dearpygui as dpg
import config as cfg
from types import SimpleNamespace


def initialize(init_flowfield):
    cfg.ff_reset_coords = init_flowfield()

def setup_args(args: SimpleNamespace):
    for arg in list(args.__dict__):
        prop = getattr(args, arg)
        if hasattr(prop, 'type') and prop.type == cfg.TYPE_SLIDER_INT:
            dpg.add_slider_int(width=cfg.sp_width/2, label=arg, parent=cfg.ff_func_settings, default_value=prop.val, max_value=prop.max_val, min_value=prop.min_val, user_data=prop, callback= lambda sender, data, property: getattr(property, 'callback')(sender, data, property) if hasattr(property, 'callback') else setattr(property, 'val', data))
        elif hasattr(prop, 'type') and prop.type == cfg.TYPE_INPUT_TEXT:
            dpg.add_input_text(width=cfg.sp_width/2, label=arg, parent=cfg.ff_func_settings, default_value=prop.val, user_data=prop, callback= lambda sender, data, property: getattr(property, 'callback')(sender, data, property) if hasattr(property, 'callback') else setattr(property, 'val', data))
        else:
            dpg.add_slider_float(width=cfg.sp_width/2, label=arg, parent=cfg.ff_func_settings, default_value=prop.val, max_value=prop.max_val, min_value=prop.min_val, user_data=prop, callback= lambda sender, data, property: getattr(property, 'callback')(sender, data, property) if hasattr(property, 'callback') else setattr(property, 'val', data))
