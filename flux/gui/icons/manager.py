from pathlib import Path
import dearpygui.dearpygui as dpg  # type: ignore
from flux.core.enums import IconID
from flux.core.types import ItemTag
from flux.gui.icons.models import IconAsset
from flux.utils.logger import get_logger

logger = get_logger(__file__)


class IconManager:
    _PARENT_DIRECTORY: Path = Path(__file__).parent
    _icon_assets: dict[IconID, IconAsset] = {}
    _texture_registry: ItemTag

    @classmethod
    def _icon_path(cls, id: IconID) -> str:
        return str(cls._PARENT_DIRECTORY / "pngs" / f"{id}.png")

    @classmethod
    def _ensure_initialized(cls) -> None:
        if not cls._icon_assets:
            cls._texture_registry = dpg.add_texture_registry()
            cls._load_all_icon_assets()

    @classmethod
    def _load_all_icon_assets(cls) -> None:
        for id in IconID:
            cls._load_icon_assets(id)

    @classmethod
    def _load_icon_assets(cls, id: IconID) -> None:
        path = cls._icon_path(id)
        width, height, channels, data = dpg.load_image(path)
        texture_tag: ItemTag = dpg.add_static_texture(
            width=width,
            height=height,
            default_value=data,
            parent=cls._texture_registry,
        )
        cls._icon_assets[id] = IconAsset(
            width=width,
            height=height,
            channels=channels,
            data=data,
            texture=texture_tag,
        )

    @classmethod
    def asset(cls, id: IconID) -> IconAsset:
        cls._ensure_initialized()
        return cls._icon_assets[id]
