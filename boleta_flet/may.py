import flet as ft
import csv

def main(page: ft.Page):
    page.title = "Boleta de Calificaciones"
    page.bgcolor = "blue"
    page.window_width = 1600
    page.window_height = 600

    # 1. Dropdown de alumnos
    lista_alumnos = ft.Dropdown(
        width=150,
        label="Alumnos",
        options=[
            ft.dropdown.Option("Mendosa Chaves David"),
            ft.dropdown.Option("Peña Martinez Javir"),
            ft.dropdown.Option("Martinez Chavarria Guadalupe"),
            ft.dropdown.Option("Peña Valdez Jose Juan"),
            ft.dropdown.Option("Mazias Perez Ismael"),
            ft.dropdown.Option("flores Marchan Uziel Tupak"),
            ft.dropdown.Option("Venegas Arenas Yair"),
        ],
    )

    # 2. Dropdowns de materias (incluyendo las nuevas)
    materias = {
        "Español": ft.Dropdown(width=150, label="Español", options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]),
        "Matemáticas": ft.Dropdown(width=150, label="Matemáticas", options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]),
        "Inglés": ft.Dropdown(width=150, label="Inglés", options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]),
        "Informática": ft.Dropdown(width=150, label="Informática", options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]),
        "Historia": ft.Dropdown(width=150, label="Historia", options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]),
        "Química": ft.Dropdown(width=150, label="Química", options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]),
        "Física": ft.Dropdown(width=150, label="Física", options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)])
    }

    label_promedio = ft.Text(value="", size=20, width=100, color="white")

    # 3. Tabla de calificaciones
    tabla_calificaciones = ft.DataTable(
        columns=[ft.DataColumn(label=ft.Text("Alumno"))] +
                [ft.DataColumn(label=ft.Text(materia)) for materia in materias.keys()] +
                [ft.DataColumn(label=ft.Text("Promedio")),
                 ft.DataColumn(label=ft.Text("Desempeño"))],
        rows=[]
    )

    # Lista para evitar duplicados
    registros_alumnos = set()

    # Función para obtener el color del semáforo
    def obtener_color_semaforo(promedio):
        if promedio >= 70:
            return "green"
        elif promedio >= 60:
            return "yellow"
        else:
            return "red"

    # 4. Función para calcular el promedio y agregar la fila a la tabla
    def calcular_promedio(e):
        # 4.1 Validación SnackBar
        if not lista_alumnos.value or not all(m.value for m in materias.values()):
            page.snack_bar = ft.SnackBar(ft.Text("Completa alumno y todas las materias."), open=True)
            page.snack_bar.open = True
            page.update()
            return

        alumno = lista_alumnos.value
        # 4.2 Evitar duplicados
        if alumno in registros_alumnos:
            page.snack_bar = ft.SnackBar(ft.Text("Este alumno ya está registrado."), open=True)
            page.snack_bar.open = True
            page.update()
            return

        notas = [int(m.value or 0) for m in materias.values()]
        promedio = sum(notas) / len(notas)
        label_promedio.value = f"{promedio:.2f}"

        # Obtener el color del semáforo
        color_semaforo = obtener_color_semaforo(promedio)
        semaforo = ft.Container(width=20, height=20, bgcolor=color_semaforo, border_radius=10)

        nueva_fila = ft.DataRow(cells=[ft.DataCell(ft.Text(alumno))] +
                                     [ft.DataCell(ft.Text(materias[materia].value or "")) for materia in materias.keys()] +
                                     [ft.DataCell(ft.Text(f"{promedio:.2f}")),
                                      ft.DataCell(semaforo)])
        tabla_calificaciones.rows.append(nueva_fila)
        registros_alumnos.add(alumno)  # Agregar alumno al conjunto de registros
        page.update()

    # 5. Botón Borrar
    def borrar_datos(e):
        for materia in materias.values():
            materia.value = None
        lista_alumnos.value = None
        label_promedio.value = ""
        page.update()
        tabla_calificaciones.rows.clear()
        registros_alumnos.clear()
        page.update()

    # 6. Botón Eliminar (elimina la última fila)
    def eliminar_ultima_fila(e):
        if tabla_calificaciones.rows:
            alumno_eliminado = tabla_calificaciones.rows[-1].cells[0].content.value
            tabla_calificaciones.rows.pop()
            registros_alumnos.remove(alumno_eliminado)
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("No hay filas para eliminar."), open=True)
            page.snack_bar.open = True
            page.update()

    # 7. Botón Exportar CSV
    def exportar_csv(e):
        if not tabla_calificaciones.rows:
            page.snack_bar = ft.SnackBar(ft.Text("No hay datos para exportar."), open=True)
            page.snack_bar.open = True
            page.update()
            return

        with open("calificaciones.csv", "w", newline="") as archivo_csv:
            writer = csv.writer(archivo_csv)
            # Escribir encabezados
            writer.writerow(["Alumno"] + list(materias.keys()) + ["Promedio"])
            # Escribir datos
            for fila in tabla_calificaciones.rows:
                datos_fila = [celda.content.value for celda in fila.cells[:-1]]  # Excluir la columna de desempeño
                writer.writerow(datos_fila)

        page.snack_bar = ft.SnackBar(ft.Text("¡CSV exportado!"), open=True)
        page.snack_bar.open = True
        page.update()

    boton_calcular = ft.ElevatedButton(text="Calcular Promedio", on_click=calcular_promedio)
    boton_borrar = ft.ElevatedButton(text="Borrar Datos", on_click=borrar_datos)
    boton_eliminar = ft.ElevatedButton(text="Eliminar Última Fila", on_click=eliminar_ultima_fila)
    boton_exportar_csv = ft.ElevatedButton(text="Exportar CSV", on_click=exportar_csv)

    # 8. Diseño de la interfaz
    fila_dropdowns = ft.Row(
        [lista_alumnos] + list(materias.values()) + [label_promedio],
        alignment=ft.MainAxisAlignment.SPACE_AROUND
    )

    fila_botones = ft.Row(
        [boton_calcular, boton_borrar, boton_eliminar, boton_exportar_csv],
        alignment=ft.MainAxisAlignment.CENTER
    )

    page.add(
        ft.Column(
            [
                fila_dropdowns,
                fila_botones,
                tabla_calificaciones
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
    )

ft.app(target=main, view=ft.WEB_BROWSER)