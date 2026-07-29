from dataclasses import dataclass
from flux.core.models import ThemeSpec, ColorPalette

DARK_THEME = ThemeSpec(
    colors=ColorPalette(
        primary_bg=(18, 18, 18, 255),
        secondary_bg=(30, 30, 30, 255),
        surface=(40, 40, 40, 255),
        surface_hover=(50, 50, 50, 255),
        border=(70, 70, 70, 255),
        primary_text=(220, 220, 220, 255),
        secondary_text=(150, 150, 150, 255),
        accent=(232, 100, 58, 255),
    )
)
