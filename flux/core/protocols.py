from typing import Protocol
from flux.core.types import ItemTag
from flux.gui.icons.models import IconAsset
from flux.core.enums import ComponentTheme, IconID


class SettingsView(Protocol):
    @property
    def tag(self) -> ItemTag: ...


class IconProvider(Protocol):
    def icon(self, icon: IconID) -> IconAsset: ...


class ThemeSubscriber(Protocol):
    def apply_theme(self) -> None: ...


class ThemeProvider(Protocol):
    def item_theme(self, componentTheme: ComponentTheme) -> ItemTag: ...
    def subscribe(self, subscriber: ThemeSubscriber) -> None: ...
