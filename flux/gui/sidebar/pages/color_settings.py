import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.types import ItemTag
from flux.gui.widgets.accordion import Accordion
from flux.gui.widgets.collapsible_panel import CollapsiblePanel


class ColorSettings:
    def __init__(self) -> None:
        self._tag: ItemTag = dpg.generate_uuid()
        self._accordion = Accordion()
        with dpg.group(tag=self._tag, show=False):
            with self._accordion.add_panel(label="Flowfield Colors", default_open=True):
                dpg.add_color_picker(
                    width=-1,
                    alpha_bar=True,
                    display_hex=True,
                    no_side_preview=True,
                )
            with self._accordion.add_panel(label="Particle Colors"):
                dpg.add_color_picker(
                    width=-1,
                    alpha_bar=True,
                    display_hex=True,
                    no_side_preview=True,
                )
                dpg.add_color_picker(
                    width=-1,
                    alpha_bar=True,
                    display_hex=True,
                    no_side_preview=True,
                )
                dpg.add_color_picker(
                    width=-1,
                    alpha_bar=True,
                    display_hex=True,
                    no_side_preview=True,
                )

    @property
    def tag(self) -> ItemTag:
        return self._tag
