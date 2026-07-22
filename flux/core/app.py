from typing import Type

from flux.__init__ import __version__
import dearpygui.dearpygui as dpg  # type: ignore


class AppConfig:
    title: str = "Flux" + __version__
    control_panel_width: int = 300
    viewport_width: int = 1200
    viewport_height: int = 750
    resizable: bool = False


class App:
    def __init__(self, config: Type[AppConfig] = AppConfig):
        dpg.create_context()
        dpg.create_viewport(
            title=config.title,
            width=config.viewport_width,
            height=config.viewport_height,
            resizable=config.resizable,
        )
        dpg.setup_dearpygui()

        # Setup UI

    def run(self) -> None:
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
