import os
import importlib
import inspect


__globals = globals()
particle_color_function_registry = {}


for file in os.listdir(os.path.dirname(__file__)):
   if not file.startswith('__') and file.endswith('.py'):
      module_name = file[:-3]
      module = importlib.import_module(f'{__name__}.{module_name}')
      __globals[module_name] = module

      for _, obj in inspect.getmembers(module):
         if inspect.isclass(obj) and obj.__module__ == module.__name__:
            particle_color_function = obj()
            particle_color_function_registry[particle_color_function.name] = particle_color_function
