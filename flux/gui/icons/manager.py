from pathlib import Path
import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.enums import IconID
from flux.core.types import ItemTag
from flux.gui.icons.models import IconAsset
from flux.utils.logger import get_logger

logger = get_logger(__file__)


class IconManager:
    PARENT_DIRECTORY = Path(__file__).parent

    def __init__(self) -> None:
        self._icons: dict[IconID, IconAsset] = {}
        self._texture_registry: ItemTag = dpg.add_texture_registry()

    def load(self, icon: IconID) -> None:
        if icon in self._icons.keys():
            return

        path = self.PARENT_DIRECTORY / "pngs" / f"{icon}.png"
        width, height, channels, data = dpg.load_image(str(path))
        texture_tag: ItemTag = dpg.add_static_texture(
            width=width,
            height=height,
            default_value=data,
            parent=self._texture_registry,
        )
        self._icons[icon] = IconAsset(
            width=width,
            height=height,
            channels=channels,
            data=data,
            texture=texture_tag,
        )

    def load_all(self) -> None:
        for icon in IconID:
            self.load(icon)

    def icon(self, icon: IconID) -> IconAsset:
        if icon not in self._icons.keys():
            logger.warning("icon not loaded yet")
            # return
        return self._icons[icon]
