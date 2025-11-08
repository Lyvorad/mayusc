import flet as ft
import asyncio
from services.text_tools import to_uppercase, to_lowercase, correct_with_ai
from theme import AppTheme

def TextToolsPage(page: ft.Page, app_state):
    initial_text = app_state.text_tools_content if hasattr(app_state, 'text_tools_content') else ""

    # Entrada de texto (área grande)
    text_input = ft.TextField(
        label="Enter your text here",
        multiline=True,
        min_lines=10,
        expand=True,
        value=initial_text,
        on_change=lambda e: setattr(app_state, 'text_tools_content', text_input.value),
        border=ft.InputBorder.OUTLINE,
        border_radius=10,
        content_padding=15,
    )

    text_container = ft.Container(
        content=text_input,
        margin=20,
        height=300,
        border=ft.border.all(1, AppTheme.get_theme(page.theme_mode)["primary"]),
        border_radius=10,
        padding=10,
    )

    # Resultado (área grande)
    result_text = ft.TextField(
        value="",
        multiline=True,
        min_lines=10,
        read_only=True,
        expand=True,
        border=ft.InputBorder.NONE,
        content_padding=15,
    )

    result_container = ft.Container(
        content=ft.Column([
            ft.Text("Corrected text:", weight=ft.FontWeight.BOLD, size=16),
            result_text
        ]),
        margin=20,
        height=300,
        border=ft.border.all(1, AppTheme.get_theme(page.theme_mode)["primary"]),
        border_radius=10,
        padding=10,
        visible=False,
    )

    copy_button = ft.ElevatedButton("Copy result", visible=False)

    def copy_result(e):
        page.set_clipboard(result_text.value)
        copy_button.text = "Copied!"
        page.update()
        page.run_task(reset_text())

    async def reset_text():
        await page.sleep(2)
        copy_button.text = "Copy result"
        page.update()

    def update_result(text):
        result_text.value = text
        result_container.visible = True
        copy_button.visible = True
        page.update()

    def handle_uppercase(e):
        update_result(to_uppercase(text_input.value))

    def handle_lowercase(e):
        update_result(to_lowercase(text_input.value))

    async def handle_ai_correction(e):
        result_text.value = "Correcting text, please wait..."
        result_container.visible = True
        copy_button.visible = False
        page.update()
        corrected = await correct_with_ai(text_input.value)
        update_result(corrected)

    # Botón AI con contenedor animado
    ai_button_text = ft.Text(
        "AI Correction",
        size=16,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
    )

    ai_button_container = ft.Container(
        content=ai_button_text,
        width=150,
        height=50,
        alignment=ft.alignment.center,
        border_radius=12,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[ft.Colors.PURPLE, ft.Colors.CYAN],
        ),
        on_click=handle_ai_correction,
        animate=ft.Animation(500, "easeInOut"),
    )

    async def animate_ai_button():
        colors = [
            ft.Colors.PURPLE,
            ft.Colors.BLUE,
            ft.Colors.CYAN,
            ft.Colors.GREEN,
            ft.Colors.YELLOW,
            ft.Colors.ORANGE,
            ft.Colors.RED,
            ft.Colors.PINK,
        ]
        i = 0
        while True:
            ai_button_container.gradient = ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[
                    colors[i % len(colors)],
                    colors[(i + 2) % len(colors)],
                ],
            )
            ai_button_container.update()
            i += 1
            await asyncio.sleep(0.3)

    page.run_task(animate_ai_button)

    # Fila de botones
    buttons = ft.Row(
        controls=[
            ft.ElevatedButton("UPPERCASE", on_click=handle_uppercase),
            ft.ElevatedButton("lowercase", on_click=handle_lowercase),
            ai_button_container,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    copy_button_row = ft.Row(
        controls=[copy_button],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # --- LISTVIEW SCROLLEABLE (main content) ---
    main_listview = ft.ListView(
        controls=[
            ft.Container(height=20),
            buttons,
            ft.Container(height=30),
            text_container,
            ft.Container(height=30),
            result_container,
            ft.Container(height=20),
            copy_button_row,
            ft.Container(height=50),
        ],
        expand=True,   # <-- importante
        spacing=10,
        padding=20,
    )

    # Envolver en un container expandible (asegura que, al añadirse en page, ocupe espacio)
    outer = ft.Container(
        content=main_listview,
        expand=True,   # <-- importante
    )

    return outer
