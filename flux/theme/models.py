from dataclasses import dataclass
from flux.core.types import Color


@dataclass(frozen=True)
class ColorPalette:
    primary_bg: Color
    secondary_bg: Color

    surface: Color
    surface_hover: Color

    border: Color

    primary_text: Color
    secondary_text: Color

    accent: Color


@dataclass(frozen=True)
class FontSpec:
    filename: str
    size: int


@dataclass(frozen=True)
class ThemeSpec:
    colors: ColorPalette
    regular_font: FontSpec
    icon_font: FontSpec
