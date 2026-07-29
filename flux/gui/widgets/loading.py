import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.protocols import HasSize
from flux.utils.logger import get_logger
from flux.core.types import ItemTag

logger = get_logger(__name__)


class Loading:
    def __init__(self, app: HasSize) -> None:
        self.app = app
        self.window: ItemTag = dpg.generate_uuid()
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
            with dpg.child_window(auto_resize_x=True, auto_resize_y=True):
                dpg.add_loading_indicator(label="Loading", style=1, radius=12, speed=1)
        dpg.set_frame_callback(3, lambda: self.center())
        # dpg.render_dearpygui_frame()
        # self.center()

    def center(self) -> None:
        vw = self.app.width
        vh = self.app.height
        w = dpg.get_item_rect_size(self.window)[0]
        h = dpg.get_item_rect_size(self.window)[1]
        dpg.set_item_pos(
            self.window,
            [
                (vw - w) // 2,
                (vh - h) // 2,
            ],
        )

    def show(self) -> None:
        dpg.show_item(self.window)
        dpg.set_frame_callback(3, lambda: self.center())

    def hide(self) -> None:
        dpg.hide_item(self.window)
