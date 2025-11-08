import flet as ft

def create_drawer(navigate_to):
    def handle_change(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            navigate_to("text_tools")
        elif selected_index == 1:
            navigate_to("settings")
        elif selected_index == 2:
            navigate_to("credits")

    return ft.NavigationDrawer(
        on_change=handle_change,
        controls=[
            ft.NavigationDrawerDestination(
                icon=ft.Icons.TEXT_FIELDS,
                label="Text Tools"
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.SETTINGS,
                label="Settings"
            ),
            ft.Divider(thickness=1),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.FAVORITE_OUTLINE,
                label="Credits & Support"
            ),
        ]
    )
