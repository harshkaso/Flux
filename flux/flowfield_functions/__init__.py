from .default import default_noise
from .swirly import swirly
import dearpygui.dearpygui as dpg
from types import SimpleNamespace
from config import ff_func_settings, sp_width

ff_funcs = {
    'Default': default_noise,
    'Swirly': swirly
}


def setup_args(args: SimpleNamespace):
    for arg in list(args.__dict__):
        attr = getattr(args, arg)
        dpg.add_slider_float(width=sp_width/2, label=arg, parent=ff_func_settings, default_value=attr.val, max_value=attr.max_val, min_value=attr.min_val, callback=lambda sender, data: setattr(attr, 'val', data))

def get_ff_func(func):
    args, noise = ff_funcs.get(func)()
    setup_args(args)        
    return noise
