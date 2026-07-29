from typing import Protocol
from flux.core.types import Color


class HasSize(Protocol):
    @property
    def width(self) -> int: ...
    @property
    def height(self) -> int: ...


class Widget(Protocol):
    def build(self) -> None: ...


class Container(Widget, Protocol):
    def build(self, *children: Widget) -> None: ...
