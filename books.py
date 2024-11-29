from nicegui import ui
from random import randint, random

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
bar_data = [randint(10, 100) for _ in months]
line_data = [randint(50, 150) for _ in months]
grouped_bar_data = {
    "A": [randint(20, 100) for _ in range(5)],
    "B": [randint(10, 80) for _ in range(5)],
}

books = [
    {"ID": 1, "Nome": "Livro 1", "Valor": "R$3000,00"},
    {"ID": 2, "Nome": "Livro 2", "Valor": "R$2500,00"},
    {"ID": 3, "Nome": "Livro 3", "Valor": "R$1500,00"},
    {"ID": 4, "Nome": "Livro 4", "Valor": "R$1000,00"},
]

def render_books_dashboard():
    # Cabeçalho
    with ui.row().classes("justify-between w-full items-center mb-4"):
        ui.label("Logo").classes("text-lg font-bold")
        ui.button("Perfil", on_click=lambda: ui.notify("Perfil clicado!"))

    ui.label("Informações gerais da planilha do mês Dezembro").classes("text-xl mb-4")

    # Gráficos
    with ui.row().classes("w-full grid grid-cols-2"):
        # Gráfico de barras simples
        with ui.card():
            ui.label("Gráfico de X (Barras)").classes("text-lg font-bold mb-2")
            ui.echart({
                'xAxis': {'type': 'category', 'data': months},
                'yAxis': {'type': 'value'},
                'series': [{'type': 'bar', 'data': bar_data}],
                'tooltip': {'trigger': 'axis'},
            }).classes("w-full h-64")

        # Gráfico de linha
        with ui.card():
            ui.label("Gráfico de X (Linha)").classes("text-lg font-bold mb-2")
            ui.echart({
                'xAxis': {'type': 'category', 'data': months},
                'yAxis': {'type': 'value'},
                'series': [{'type': 'line', 'data': line_data}],
                'tooltip': {'trigger': 'axis'},
            }).classes("w-full h-64")

        # Gráfico de barras agrupadas
        with ui.card().classes("col-span-2"):
            ui.label("Gráfico de X (Barras Agrupadas)").classes("text-lg font-bold mb-2")
            ui.echart({
                'xAxis': {'type': 'category', 'data': [f"Grupo {i}" for i in range(1, 6)]},
                'yAxis': {'type': 'value'},
                'series': [
                    {'type': 'bar', 'name': 'A', 'data': grouped_bar_data["A"]},
                    {'type': 'bar', 'name': 'B', 'data': grouped_bar_data["B"]},
                ],
                'tooltip': {'trigger': 'axis'},
                'legend': {'data': ['A', 'B']},
            }).classes("w-full h-64")

    # Tabela de livros
    ui.label("Livros").classes("text-xl mt-6 mb-4")
    columns = [
      {'name': 'ID', 'label': 'Id', 'field': 'ID', 'required': True, 'align': 'left'},
      {'name': 'Nome', 'label': 'Nome', 'field': 'Nome'},
      {'name': 'Valor', 'label': 'Valor', 'field': 'Valor'},
    ]
    ui.table(columns=columns, rows=books, row_key='name').classes("w-full")
