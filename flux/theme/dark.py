from flux.theme.models import ThemeSpec, ColorPalette

DARK_THEME = ThemeSpec(
    colors=ColorPalette(
        primary_bg=(18, 18, 18, 255),
        secondary_bg=(39, 39, 37, 255),
        surface=(55, 55, 53, 255),
        surface_hover=(65, 65, 63, 255),
        border=(80, 80, 78, 255),
        primary_text=(220, 220, 220, 255),
        secondary_text=(150, 150, 150, 255),
        accent=(232, 100, 58, 255),
    )
)
