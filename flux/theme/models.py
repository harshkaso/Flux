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
class Spacing:
    xs: int
    sm: int
    md: int
    lg: int
    xl: int

    sidebar_padding: int
    section_gap: int


@dataclass(frozen=True)
class Typography:
    font_family: str

    body_size: int
    heading_size: int
    monospace_size: int


@dataclass(frozen=True)
class ThemeSpec:
    colors: ColorPalette
    spacing: Spacing | None = None
    typography: Typography | None = None
