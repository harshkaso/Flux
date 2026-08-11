import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.types import ItemTag


class ColorSettings:
    def __init__(self) -> None:
        self._tag: ItemTag = dpg.generate_uuid()
        with dpg.group(tag=self._tag, show=False):
            ...

    @property
    def tag(self) -> ItemTag:
        return self._tag
