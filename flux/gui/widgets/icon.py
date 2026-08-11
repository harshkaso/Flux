import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.enums import IconID
from flux.core.types import ItemTag
from flux.gui.icons.manager import IconManager
from flux.gui.icons.models import IconAsset
from flux.utils.logger import get_logger

logger = get_logger(__name__)


class IconWidget:
    def __init__(self, *, icon: IconID, pos: list[int] | tuple[int, ...] = []) -> None:
        self._image: ItemTag = dpg.generate_uuid()
        self._asset: IconAsset = IconManager.asset(icon)
        dpg.add_image(tag=self._image, texture_tag=self._asset.texture, pos=pos)

    def update(self, new_icon: IconID) -> None:
        self._asset = IconManager.asset(new_icon)
        dpg.configure_item(self._image, texture_tag=self._asset.texture)

    @property
    def width(self) -> int:
        return self._asset.width

    @property
    def height(self) -> int:
        return self._asset.height
