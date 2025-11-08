import flet as ft

def create_drawer(navigate_callback):
    return ft.NavigationDrawer(
        controls=[
            ft.Container(height=20),
            ft.Text("Menu", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Divider(),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.TEXT_FIELDS, label="Text Tools", selected_icon=ft.Icons.TEXT_FIELDS_OUTLINED
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.SETTINGS, label="Settings", selected_icon=ft.Icons.SETTINGS_OUTLINED
            ),
        ],
        on_change=lambda e: navigate_callback(
            "text_tools" if e.control.selected_index == 0 else "settings"
        ),
    )
