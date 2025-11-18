import flet as ft

class AppTheme:
    # Colores celestes para modo claro
    PRIMARY_LIGHT = "#87CEEB"  # Celeste claro
    SECONDARY_LIGHT = "#B0E2FF"  # Celeste más claro
    BG_LIGHT = ft.Colors.BLUE_50  # Blanco
    SURFACE_LIGHT = "#F0F8FF"  # Azul muy claro
    TEXT_LIGHT = "#333333"  # Texto oscuro
    
    # Colores para modo oscuro
    PRIMARY_DARK = "#4682B4"  # Azul acero
    SECONDARY_DARK = "#5F9EA0"  # Azul cadete
    BG_DARK = "#121212"  # Negro
    SURFACE_DARK = "#1E1E1E"  # Gris oscuro
    TEXT_DARK = "#FFFFFF"  # Texto blanco
    
    @staticmethod
    def get_theme(theme_mode: ft.ThemeMode):
        if theme_mode == ft.ThemeMode.DARK:
            return {
                "primary": AppTheme.PRIMARY_DARK,
                "secondary": AppTheme.SECONDARY_DARK,
                "bgcolor": AppTheme.BG_DARK,
                "surface": AppTheme.SURFACE_DARK,
                "text_color": AppTheme.TEXT_DARK
            }
        else:
            return {
                "primary": AppTheme.PRIMARY_LIGHT,
                "secondary": AppTheme.SECONDARY_LIGHT,
                "bgcolor": AppTheme.BG_LIGHT,
                "surface": AppTheme.SURFACE_LIGHT,
                "text_color": AppTheme.TEXT_LIGHT
            }