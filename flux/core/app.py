import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.state import State
from flux.core.enums import ComponentTheme
from flux.gui.app_window import AppWindow
from flux.theme.manager import ThemeManager
from flux.utils.logger import setup_logger, get_logger, shutdown_loggers

logger = get_logger(__name__)


class App:
    DEFAULT_TITLE = "Flux"
    DEFAULT_VIEWPORT_WIDTH = 1440
    DEFAULT_VIEWPORT_HEIGHT = 900
    DEFAULT_RESIZABLE = False

    def __init__(
        self,
        *,
        title: str = DEFAULT_TITLE,
        viewport_width: int = DEFAULT_VIEWPORT_WIDTH,
        viewport_height: int = DEFAULT_VIEWPORT_HEIGHT,
        resizable: bool = DEFAULT_RESIZABLE,
    ) -> None:
        dpg.create_context()
        dpg.create_viewport(
            title=title,
            width=viewport_width,
            height=viewport_height,
            resizable=resizable,
        )
        dpg.setup_dearpygui()
        self.app_window = AppWindow()

    def start(self) -> None:
        dpg.show_viewport()
        dpg.show_font_manager()
        dpg.show_item_registry()
        # dpg.show_style_editor()
        # dpg.show_metrics()
        try:
            ThemeManager.subscribe(self)
            self.apply_theme()
            dpg.set_primary_window(self.app_window.tag, True)
            dpg.set_exit_callback(self.close_app)

            self.run()
        except Exception:
            logger.error("error occured when starting application", exc_info=True)
        finally:
            dpg.destroy_context()

    def run(self) -> None:
        # count = 0
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()

    def apply_theme(self) -> None:
        dpg.bind_font(ThemeManager.regular_font())
        dpg.bind_theme(ThemeManager.item_theme(ComponentTheme.APPLICATION))

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
