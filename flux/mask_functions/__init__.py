import os
import importlib
import dearpygui.dearpygui as dpg
import config as cfg
from types import SimpleNamespace

__globals = globals()
__mask_funcs = {}
for file in os.listdir(os.path.dirname(__file__)):
    mod_name = file[:-3]   # strip .py at the end
    if not mod_name.startswith('__'): # Avoid importing __init__.py
        __globals[mod_name] = importlib.import_module('.' + mod_name, package=__name__)
        __mask_funcs[__globals[mod_name].get_mask_function_name()] = __globals[mod_name].mask 


def _setup_args(args: SimpleNamespace):
    for arg in list(args.__dict__):
        prop = getattr(args, arg)
        if hasattr(prop, 'type') and prop.type == cfg.TYPE_SLIDER_INT:
            dpg.add_slider_int(width=cfg.sp_width/2, label=arg, parent=cfg.mask_settings, default_value=prop.val, max_value=prop.max_val, min_value=prop.min_val, user_data=prop, callback= lambda sender, data, property: getattr(property, 'callback')(sender, data, property) if hasattr(property, 'callback') else setattr(property, 'val', data))
        elif hasattr(prop, 'type') and prop.type == cfg.TYPE_INPUT_TEXT:
            dpg.add_input_text(width=cfg.sp_width/2, label=arg, parent=cfg.mask_settings, default_value=prop.val, user_data=prop, callback= lambda sender, data, property: getattr(property, 'callback')(sender, data, property) if hasattr(property, 'callback') else setattr(property, 'val', data))
        else:
            dpg.add_slider_float(width=cfg.sp_width/2, label=arg, parent=cfg.mask_settings, default_value=prop.val, max_value=prop.max_val, min_value=prop.min_val, user_data=prop, callback= lambda sender, data, property: getattr(property, 'callback')(sender, data, property) if hasattr(property, 'callback') else setattr(property, 'val', data))

def get_mask_function(func):
    args, calc_mask = __mask_funcs.get(func)()
    if args:
        _setup_args(args)        
    return SimpleNamespace(calc_mask=calc_mask)


def get_mask_function_names():
    return list(__mask_funcs.keys())
