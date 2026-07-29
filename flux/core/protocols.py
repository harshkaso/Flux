from typing import Protocol
from flux.core.types import Color, ItemTag
from flux.core.models import ThemeSpec


class HasSize(Protocol):
    @property
    def width(self) -> int: ...
    @property
    def height(self) -> int: ...


class Widget(Protocol):
    def build(self) -> None: ...


class Container(Widget, Protocol):
    def build(self, *children: Widget) -> None: ...


class Themeable(Protocol):
    def apply_theme(self) -> None: ...


class ThemeBuilder(Protocol):
    def build(self, theme: ThemeSpec) -> ItemTag: ...
