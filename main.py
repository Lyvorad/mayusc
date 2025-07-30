import flet as ft
from chtgpt import corregir  # Importamos la función

def main(page: ft.Page):
    page.title = "Convertir texto"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    texto_input = ft.TextField(
        label="Pega tu texto aquí",
        multiline=True,
        height=200,
        expand=True,
    )

    resultado_texto = ft.Text(value="", selectable=True, weight=ft.FontWeight.BOLD)

    resultado_scroll = ft.Column(
        controls=[resultado_texto],
        scroll="auto",
        height=200,
        expand=True,
    )

    boton_copiar = ft.ElevatedButton(
        "Copiar resultado",
        visible=False,  # Invisible hasta que haya texto corregido
    )

    def copiar_resultado(e):
        page.set_clipboard(resultado_texto.value)
        # Puedes agregar feedback, ejemplo:
        boton_copiar.text = "¡Copiado!"
        page.update()
        # Opcional: volver al texto original después de 2 seg
        def reset_text(e):
            boton_copiar.text = "Copiar resultado"
            page.update()
        page.timer(2000, reset_text)

    boton_copiar.on_click = copiar_resultado

    resultado_contenedor = ft.Container(
        content=ft.Column([resultado_scroll, boton_copiar]),
        padding=10,
        bgcolor="#e0e0e0",
        border_radius=5,
        border=ft.border.all(1, "#888888"),
        height=250,
        expand=True,
        visible=False
    )

    # Funciones para conversión
    def convertir_mayusculas(e):
        texto_original = texto_input.value
        resultado_texto.value = texto_original.upper()
        boton_copiar.visible = False
        resultado_contenedor.visible = True
        page.update()

    def convertir_minusculas(e):
        texto_original = texto_input.value
        resultado_texto.value = texto_original.lower()
        boton_copiar.visible = False
        resultado_contenedor.visible = True
        page.update()

    def corregir_texto(e):
        texto_original = texto_input.value
        resultado_texto.value = "Corrigiendo texto, por favor espera..."
        boton_copiar.visible = False
        resultado_contenedor.visible = True
        page.update()

        try:
            texto_corregido = corregir(texto_original)
            resultado_texto.value = texto_corregido
            boton_copiar.visible = True  # Mostrar botón copiar solo si hay texto corregido
        except Exception as err:
            resultado_texto.value = f"Error al corregir: {err}"
            boton_copiar.visible = False

        page.update()

    def apoyar_dinero(e):
        page.launch_url("https://paypal.me/lyvorad")

    # Botones
    boton_mayusculas = ft.ElevatedButton("MAYÚSCULAS", on_click=convertir_mayusculas)
    boton_minusculas = ft.ElevatedButton("minúsculas", on_click=convertir_minusculas)
    boton_corregir = ft.ElevatedButton("Corregir", on_click=corregir_texto)
    boton_donar = ft.TextButton(
        content=ft.Row([
            ft.Icon(name=ft.Icons.FAVORITE, color=ft.Colors.RED),
            ft.Text("Apóyanos para seguir creciendo")
        ], alignment=ft.MainAxisAlignment.CENTER),
        on_click=apoyar_dinero
    )

    botones_fila = ft.Row(
        controls=[boton_mayusculas, boton_minusculas, boton_corregir],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    contenido = ft.Container(
        content=ft.Column(
            controls=[botones_fila, texto_input, resultado_contenedor, boton_donar],
            spacing=20,
            width=float("inf"),
        ),
        padding=20,
        width=600,
    )

    page.add(contenido)

ft.app(target=main)


