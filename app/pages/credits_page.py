import flet as ft
from theme import AppTheme

def CreditsPage(page: ft.Page):
    theme = AppTheme.get_theme(page.theme_mode)

    # Title
    title = ft.Text(
        "Credits & Support",
        size=26,
        weight=ft.FontWeight.BOLD,
        color=theme["text_color"],
        text_align=ft.TextAlign.CENTER,
    )

    # Description text
    description = ft.Text(
        "This project was created with dedication and creativity to make writing easier for everyone.\n\n"
        "We sincerely thank everyone who believed in this project and supported it in any way.",
        size=16,
        color=theme["text_color"],
        text_align=ft.TextAlign.CENTER,
    )

    # Flet emoji heart
    heart = ft.Text("❤️", size=30, text_align=ft.TextAlign.CENTER)

    # Donation button
    def open_donation_link(e):
        page.launch_url("https://paypal.me/lyvorad")

    donate_button = ft.ElevatedButton(
        text="Support this Project",
        icon=ft.Icons.VOLUNTEER_ACTIVISM_OUTLINED,
        bgcolor=theme["primary"],
        color=ft.Colors.WHITE,
        on_click=open_donation_link,
    )

    # Layout
    content = ft.Column(
        [
            title,
            ft.Container(height=20),
            description,
            ft.Container(height=10),
            heart,
            ft.Container(height=25),
            donate_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        spacing=15,
    )

    # Outer container (ensures visibility and expansion)
    return ft.Container(
        content=content,
        expand=True,
        bgcolor=theme["bgcolor"],
        alignment=ft.alignment.center,
        padding=30,
    )
