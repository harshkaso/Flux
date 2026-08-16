from flux.theme.models import FontSpec, ThemeSpec, ColorPalette

LIGHT_THEME = ThemeSpec(
    colors=ColorPalette(
        primary_bg=(248, 248, 248, 255),
        secondary_bg=(238, 238, 238, 255),
        surface=(255, 255, 255, 255),
        surface_hover=(245, 245, 245, 255),
        border=(210, 210, 210, 255),
        primary_text=(33, 33, 33, 255),
        secondary_text=(102, 102, 102, 255),
        accent=(232, 100, 58, 255),
    ),
    regular_font=FontSpec(filename="IBMPlexMono-Regular.ttf", size=15),
    icon_font=FontSpec(filename="flux-icons.ttf", size=24),
)
