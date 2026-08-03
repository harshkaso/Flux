from flux.__init__ import __version__
import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.state import State
from flux.core.types import ItemTag
from flux.core.enums import ComponentTheme
from flux.gui.app_window import AppWindow
from flux.gui.overlay import OverlayManager
from flux.theme.manager import ThemeManager
from flux.utils.logger import setup_logger, get_logger, shutdown_loggers

logger = get_logger(__name__)


class AppConfig:
    def __init__(self) -> None:
        self.title: str = "Flux-" + __version__
        self.control_panel_width: int = 300
        self.viewport_width: int = 1440
        self.viewport_height: int = 900
        self.resizable: bool = False


class App:
    def __init__(self, config: AppConfig = AppConfig()):
        dpg.create_context()
        dpg.create_viewport(
            title=config.title,
            width=config.viewport_width,
            height=config.viewport_height,
            resizable=config.resizable,
        )
        dpg.setup_dearpygui()
        self.theme = ThemeManager()
        # self.state = State()
        # self.overlay = OverlayManager()
        # self.sidebar = Sidebar(self, width=config.control_panel_width)
        # self.canvas = Canvas(self)
        self.app_window = AppWindow(self)

    def start(self) -> None:
        dpg.show_viewport()
        try:
            self.theme.subscribe(self)
            self.apply_theme()
            dpg.set_primary_window(self.app_window.window, True)
            dpg.set_exit_callback(self.close_app)

            self.run()
        except Exception:
            logger.error("error occured when starting application", exc_info=True)
        finally:
            dpg.destroy_context()

    def run(self) -> None:
        # count = 0
        while dpg.is_dearpygui_running():
            # count += 1
            # if count == 100:
            # self.overlay.show_loading(message="Finally Flux is loaded")
            # if count == 200:
            #     self.overlay.hide()
            dpg.render_dearpygui_frame()

    def apply_theme(self) -> None:
        dpg.bind_theme(self.theme.item_theme(ComponentTheme.APPLICATION))

    def close_app(self) -> None:
        # TODO: Handle cleanup tasks on exiting.
        logger.info("closing the application")

    @property
    def width(self) -> int:
        return dpg.get_viewport_client_width()

    @property
    def height(self) -> int:
        return dpg.get_viewport_client_height()


def bootstrap() -> int:
    setup_logger()
    try:
        app = App()
        app.start()
        logger.info("application exited successfully.")
        return 0
    except KeyboardInterrupt:
        logger.warning("application interrupted by user.")
        return 0
    except Exception:
        logger.error("an error occured while running the application", exc_info=True)
        return 1
    finally:
        shutdown_loggers()
