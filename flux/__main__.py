import sys
import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.app import bootstrap

if __name__ == "__main__":
    sys.exit(bootstrap())
