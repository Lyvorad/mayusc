import flet as ft
from components.app_bar import create_appbar
from components.nav_drawer import create_drawer
from pages.text_tools_page import TextToolsPage
from pages.settings_page import SettingsPage
from pages.credits_page import CreditsPage
from theme import AppTheme

class AppState:
    def __init__(self):
        self.text_tools_content = ""
        self.current_theme = ft.ThemeMode.LIGHT

def main(page: ft.Page):
    page.title = "Text Tools App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = AppTheme.BG_LIGHT
    
    # Inicializar estado de la app
    app_state = AppState()
    
    # Página inicial (expand=True para permitir scroll)
    current_page = ft.Container(
        content=TextToolsPage(page, app_state),
        expand=True
    )

    # Función para cambiar páginas
    def navigate_to(route: str):
        if route == "text_tools":
            current_page.content = TextToolsPage(page, app_state)
        elif route == "settings":
            current_page.content = SettingsPage(page)
        elif route == "credits":
            current_page.content = CreditsPage(page)  # nueva página
        page.drawer.open = False
        page.update()

    # Drawer y AppBar
    page.drawer = create_drawer(navigate_to)
    page.appbar = create_appbar(page)

    # Añadir página expandida
    page.add(current_page)

ft.app(target=main)
