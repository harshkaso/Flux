import os
import importlib
import inspect

__globals = globals()
flowfield_registry = {}

for file in os.listdir(os.path.dirname(__file__)):
   if not file.startswith('__') and file.endswith('.py'):
      module_name = file[:-3]
      module = importlib.import_module(f'{__name__}.{module_name}')
      __globals[module_name] = module

      for _, obj in inspect.getmembers(module):
         if inspect.isclass(obj) and obj.__module__ == module.__name__:
            flowfield = obj()
            flowfield_registry[flowfield.name] = flowfield










# from inspect import isclass
# from pkgutil import iter_modules
# from pathlib import Path
# from importlib import import_module

# # iterate through the modules in the current package
# package_dir = Path(__file__).resolve().parent
# for (_, module_name, _) in iter_modules([package_dir]):

#     # import the module and iterate through its attributes
#     module = import_module(f"{__name__}.{module_name}")
#     for attribute_name in dir(module):
#         attribute = getattr(module, attribute_name)

#         if isclass(attribute):     
#             print(attribute)       
#             # Add the class to this package's variables
#             globals()[attribute_name] = attribute