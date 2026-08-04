from dataclasses import dataclass
from flux.core.types import ItemTag


@dataclass(frozen=True, slots=True)
class IconAsset:
    width: int
    height: int
    channels: int
    data: list[float] | tuple[float, ...]
    texture: ItemTag
