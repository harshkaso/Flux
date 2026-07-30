import dearpygui.dearpygui as dpg  # type: ignore
from flux.utils.logger import get_logger
from flux.core.types import ItemTag

logger = get_logger(__name__)


class OverlayManager:
    def __init__(self) -> None:
        self._window: ItemTag | None = None
        self._alert: ItemTag | None = None
        self._loading: ItemTag | None = None
        self._active_overlay: ItemTag | None = None

    @property
    def window(self) -> ItemTag | None:
        return self._window

    def build(self) -> None:
        if self._window:
            return
        with dpg.window(
            modal=True,
            autosize=True,
            no_close=True,
            no_move=True,
            no_title_bar=True,
            no_background=True,
            menubar=False,
            show=True,
        ) as self._window:
            # TODO: build containers for error, loading, alert messages here

            with dpg.child_window() as self.loading:
                dpg.add_loading_indicator()

    def center(self) -> None:
        vw = dpg.get_viewport_client_width()
        vh = dpg.get_viewport_client_height()
        w = dpg.get_item_rect_size(self._window)[0]
        h = dpg.get_item_rect_size(self._window)[1]
        dpg.set_item_pos(
            self._window,
            [
                (vw - w) // 2,
                (vh - h) // 2,
            ],
        )

    def show_loading(self, message: str = "Loading"):
        if self._active_overlay:
            self.hide_overlay()

        dpg.show_item(self._loading)

    def hide_overlay(self):
        if self._active_overlay == None:
            return
        dpg.hide_item(self._active_overlay)
