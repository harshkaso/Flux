import os
import importlib
import dearpygui.dearpygui as dpg
import config as cfg
from utils.flowfield import initialize, setup_args
from types import SimpleNamespace
from config import ff_func_settings, sp_width

__globals = globals()
__ff_funcs = {}
for file in os.listdir(os.path.dirname(__file__)):
    mod_name = file[:-3]   # strip .py at the end
    if not mod_name.startswith('__'): # Avoid importing __init__.py
        __globals[mod_name] = importlib.import_module('.' + mod_name, package=__name__)
        __ff_funcs[__globals[mod_name].get_flowfield_function_name()] = __globals[mod_name].flowfield 

def get_flowfield_function(func):
    args, noise, init_flowfield = __ff_funcs.get(func)()
    if args:
        setup_args(args)        
    initialize(init_flowfield)
    return SimpleNamespace(noise=noise, init_flowfield=init_flowfield)

def get_flowfield_function_names():
    return list(__ff_funcs.keys())
