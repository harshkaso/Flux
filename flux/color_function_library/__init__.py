import os
import sys
import importlib.util
import inspect

USER_PLUGIN_FOLDER_NAME = "user_color_plugins"
particle_color_function_registry = {}

# Determine the directory of the executable
if getattr(sys, 'frozen', False):
    # If the application is run as a bundled executable (e.g., by PyInstaller or Nuitka)
    executable_dir = os.path.dirname(sys.executable)
else:
    # If run as a normal script, plugins could be relative to the script or a defined project root.
    # For simplicity in this context, let's assume if not frozen, it's relative to the current working directory
    # or the script's directory. For Nuitka, sys.executable might point to the right place even when not "frozen" in PyInstaller's sense.
    # A more robust solution for non-frozen might involve finding the project root.
    # For Nuitka, os.path.dirname(os.path.abspath(__file__)) might point inside the bundled .dist folder if __file__ is used.
    # Using sys.executable is generally more reliable for finding the location of the running executable.
    executable_dir = os.path.dirname(os.path.abspath(sys.argv[0])) # sys.argv[0] can be more reliable for script path

plugin_dir = os.path.join(executable_dir, USER_PLUGIN_FOLDER_NAME)

print(f"Attempting to load user color plugins from: {plugin_dir}")

# Create the plugin directory if it doesn't exist
try:
    os.makedirs(plugin_dir, exist_ok=True)
    print(f"Ensured user plugin folder exists: {plugin_dir}")
except OSError as e:
    print(f"Error creating plugin directory {plugin_dir}: {e}. Skipping user plugins.")
    # Do not proceed if directory creation failed critically

if os.path.isdir(plugin_dir):
    for file_name in os.listdir(plugin_dir):
        if file_name.endswith('.py') and not file_name.startswith('__'):
            module_name = f"user_plugin_{file_name[:-3]}" # Prefix to avoid name collisions
            file_path = os.path.join(plugin_dir, file_name)

            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    # Adding to sys.modules is generally done so that imports within the loaded module work as expected.
                    # sys.modules[module_name] = module
                    spec.loader.exec_module(module)

                    print(f"Successfully loaded module: {module_name} from {file_path}")

                    for _, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and hasattr(obj, 'name') and obj.__module__ == module_name:
                            # Ensure the class is defined in the loaded module, not imported into it.
                            try:
                                instance = obj()
                                if hasattr(instance, 'name'):
                                    particle_color_function_registry[instance.name] = instance
                                    print(f"Registered plugin: {instance.name} from {module_name}")
                                else:
                                    print(f"Class {obj.__name__} in {module_name} does not have a 'name' attribute after instantiation.")
                            except Exception as e:
                                print(f"Error instantiating or registering class {obj.__name__} from {module_name}: {e}")
                else:
                    print(f"Could not create spec for module: {module_name} from {file_path}")
            except Exception as e:
                print(f"Error loading plugin module {module_name} from {file_path}: {e}")
else:
    # This case should ideally not be reached if os.makedirs succeeded or didn't error out.
    print(f"User plugin folder '{plugin_dir}' is not a directory. Skipping user plugins.")

# Note: The original logic for loading built-in plugins from the same directory has been removed
# as per the instructions. If built-in plugins are still desired, they would need separate loading logic.

print(f"Final particle_color_function_registry: {particle_color_function_registry.keys()}")
