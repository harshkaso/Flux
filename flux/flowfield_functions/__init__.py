from .default import default_noise
from .swirly import swirly
from .chladni_like import chladni_like
import dearpygui.dearpygui as dpg
from types import SimpleNamespace
from config import ff_func_settings, sp_width

ff_funcs = {
    'Default': default_noise,
    'Swirly': swirly,
    'Quattro': chladni_like
}

def setup_args(args: SimpleNamespace):
    for arg in list(args.__dict__):
        prop = getattr(args, arg)
        dpg.add_slider_float(width=sp_width/2, label=arg, parent=ff_func_settings, default_value=prop.val, max_value=prop.max_val, min_value=prop.min_val, user_data=prop, callback=lambda sender, data, property: setattr(property, 'val', data))

def get_ff_func(func):
    args, noise = ff_funcs.get(func)()
    setup_args(args)        
    return noise
