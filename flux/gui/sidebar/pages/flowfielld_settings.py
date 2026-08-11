import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.enums import IconID
from flux.core.types import ItemTag
from flux.gui.widgets.button import ButtonWidget


class FlowfieldSettings:
    def __init__(self) -> None:
        self._tag: ItemTag = dpg.generate_uuid()
        with dpg.group(tag=self._tag, show=False):
            ButtonWidget(label="Flowfield Settings", icon=IconID.CHEVRON_RIGHT)

    @property
    def tag(self) -> ItemTag:
        return self._tag
