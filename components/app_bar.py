import flet as ft
from theme import AppTheme

def create_appbar(page: ft.Page) -> ft.AppBar:
    def open_drawer(e):
        page.drawer.open = True
        page.update()

    theme = AppTheme.get_theme(page.theme_mode)
    
    return ft.AppBar(
        leading=ft.IconButton(icon=ft.Icons.MENU, on_click=open_drawer),
        title=ft.Text("Text Tools App", size=20, weight=ft.FontWeight.BOLD),
        bgcolor=theme["primary"],
        center_title=True,
    )