import dearpygui.dearpygui as dpg  # type: ignore
from flux.utils.logger import get_logger
from flux.core.types import ItemTag

logger = get_logger(__name__)


class OverlayManager:
    def __init__(self) -> None:
        self.window: ItemTag = dpg.generate_uuid()

    def build(self) -> None:
        with dpg.window(
            tag=self.window,
            modal=True,
            autosize=True,
            no_close=True,
            no_move=True,
            no_title_bar=True,
            no_background=True,
            menubar=False,
            show=True,
        ):
            pass

    def center(self) -> None:
        vw = dpg.get_viewport_client_width()
        vh = dpg.get_viewport_client_height()
        w = dpg.get_item_rect_size(self.window)[0]
        h = dpg.get_item_rect_size(self.window)[1]
        dpg.set_item_pos(
            self.window,
            [
                (vw - w) // 2,
                (vh - h) // 2,
            ],
        )
