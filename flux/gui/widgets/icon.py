import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.enums import IconID
from flux.core.protocols import IconProvider
from flux.core.types import ItemTag
from flux.gui.icons.models import IconAsset
from flux.utils.logger import get_logger

logger = get_logger(__name__)


class IconWidget:
    def __init__(self, icon: IconID, icon_provider: IconProvider) -> None:
        self._image: ItemTag = dpg.generate_uuid()
        self._provider: IconProvider = icon_provider
        self._asset: IconAsset = icon_provider.icon(icon)
        dpg.add_image(tag=self._image, texture_tag=self._asset.texture)

    def update(self, new_icon: IconID) -> None:
        self._asset = self._provider.icon(new_icon)
        dpg.configure_item(self._image, texture_tag=self._asset.texture)
