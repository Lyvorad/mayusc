import flet as ft
import asyncio

async def main(page: ft.Page):
    page.title = "Botón mágico 🌈"
    page.bgcolor = ft.Colors.BLACK
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER

    colores = [
        ft.Colors.RED,
        ft.Colors.ORANGE,
        ft.Colors.YELLOW,
        ft.Colors.GREEN,
        ft.Colors.CYAN,
        ft.Colors.BLUE,
        ft.Colors.PURPLE,
        ft.Colors.PINK,
    ]

    texto = ft.Text(
        "✨ ¡MAGIA! ✨",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
    )

    boton_magico = ft.Container(
        content=texto,
        width=250,
        height=80,
        alignment=ft.alignment.center,
        border_radius=20,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[ft.Colors.PURPLE, ft.Colors.CYAN],
        ),
        on_click=lambda e: page.snack_bar.open("✨ ¡Botón presionado! ✨"),
        animate=ft.Animation(500, "easeInOut"),
    )

    page.add(boton_magico)

    async def animar_gradiente():
        i = 0
        while True:
            boton_magico.gradient = ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=[
                    colores[i % len(colores)],
                    colores[(i + 2) % len(colores)],
                ],
            )
            boton_magico.update()
            i += 1
            await asyncio.sleep(0.3)

    # ✅ CORRECTO
    page.run_task(animar_gradiente)

ft.app(target=main)
