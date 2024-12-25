import os
import importlib
import dearpygui.dearpygui as dpg
import config as cfg
from types import SimpleNamespace
from config import ff_func_settings, sp_width

__globals = globals()
__ff_funcs = {}
for file in os.listdir(os.path.dirname(__file__)):
    mod_name = file[:-3]   # strip .py at the end
    if not mod_name.startswith('__'): # Avoid importing __init__.py
        __globals[mod_name] = importlib.import_module('.' + mod_name, package=__name__)
        __ff_funcs[__globals[mod_name].get_flowfield_function_name()] = __globals[mod_name].flowfield 


def _setup_args(args: SimpleNamespace):
    for arg in list(args.__dict__):
        prop = getattr(args, arg)
        # callback =  getattr(args, 'callback', lambda sender, data, property: callback if hasattr(arg, 'callback') else setattr(property, 'val', data))
        # dpg.add_slider_float(width=sp_width/2, label=arg, parent=ff_func_settings, default_value=prop.val, max_value=prop.max_val, min_value=prop.min_val, user_data=prop, callback= print(getattr(arg, callback)) if hasattr(arg, 'callback') else lambda sender, data, property: setattr(property, 'val', data))
        if hasattr(prop, 'type') and prop.type == cfg.TYPE_SLIDER_INT:
            dpg.add_slider_int(width=sp_width/2, label=arg, parent=ff_func_settings, default_value=prop.val, max_value=prop.max_val, min_value=prop.min_val, user_data=prop, callback= lambda sender, data, property: getattr(property, 'callback')(sender, data, property) if hasattr(property, 'callback') else setattr(property, 'val', data))
        elif hasattr(prop, 'type') and prop.type == cfg.TYPE_INPUT_TEXT:
            dpg.add_input_text(width=sp_width/2, label=arg, parent=ff_func_settings, default_value=prop.val, user_data=prop, callback= lambda sender, data, property: getattr(property, 'callback')(sender, data, property) if hasattr(property, 'callback') else setattr(property, 'val', data))
        else:
            dpg.add_slider_float(width=sp_width/2, label=arg, parent=ff_func_settings, default_value=prop.val, max_value=prop.max_val, min_value=prop.min_val, user_data=prop, callback= lambda sender, data, property: getattr(property, 'callback')(sender, data, property) if hasattr(property, 'callback') else setattr(property, 'val', data))

def get_flowfield_function(func):
    args, noise, init_flowfield = __ff_funcs.get(func)()
    _setup_args(args)        
    init_flowfield()
    return SimpleNamespace(noise=noise, init_flowfield=init_flowfield)

def get_flowfield_function_names():
    return list(__ff_funcs.keys())
