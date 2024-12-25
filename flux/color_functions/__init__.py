import os
import importlib

__globals = globals()
__clr_funcs = {}
for file in os.listdir(os.path.dirname(__file__)):
    mod_name = file[:-3]   # strip .py at the end
    if not mod_name.startswith('__'): # Avoid importing __init__.py
        __globals[mod_name] = importlib.import_module('.' + mod_name, package=__name__)
        __clr_funcs[__globals[mod_name].get_color_function_name()] = __globals[mod_name].color 

def get_color_function(func):
    return __clr_funcs.get(func)

def get_color_function_names():
    return list(__clr_funcs.keys())
