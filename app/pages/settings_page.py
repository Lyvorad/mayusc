import flet as ft
from theme import AppTheme

def SettingsPage(page: ft.Page):
    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
        
        theme = AppTheme.get_theme(page.theme_mode)
        page.bgcolor = theme["bgcolor"]
        page.update()

    theme = AppTheme.get_theme(page.theme_mode)
    
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Settings", size=22, weight=ft.FontWeight.BOLD, color=theme["text_color"]),
                ft.Row(
                    [
                        ft.Text("Dark Mode:", color=theme["text_color"]),
                        ft.Switch(on_change=toggle_theme, value=page.theme_mode == ft.ThemeMode.DARK)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        bgcolor=theme["bgcolor"],
    )