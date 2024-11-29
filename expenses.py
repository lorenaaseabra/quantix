from nicegui import ui
from random import randint, random

# Dados fictícios para as páginas
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
pie_data = [{"value": randint(10, 100), "name": f"Categoria {i}"} for i in range(1, 6)]

expenses = [
    {"ID": 1, "Nome": "Despesa 1", "Valor": "R$3000,00"},
    {"ID": 2, "Nome": "Despesa 2", "Valor": "R$2500,00"},
    {"ID": 3, "Nome": "Despesa 3", "Valor": "R$1500,00"},
    {"ID": 4, "Nome": "Despesa 4", "Valor": "R$1000,00"},
]

def render_expenses_dashboard():
    # Cabeçalho
    with ui.row().classes("justify-between w-full items-center mb-4"):
        ui.label("Logo").classes("text-lg font-bold")
        ui.button("Perfil", on_click=lambda: ui.notify("Perfil clicado!"))

    ui.label("Informações gerais da planilha do mês Dezembro").classes("text-xl mb-4")

    # Gráficos
    with ui.row().classes("w-full grid grid-cols-2"):
        # Gráfico de pizza 1
        with ui.card():
            ui.label("Gráfico de X (Pizza 1)").classes("text-lg font-bold mb-2")
            ui.echart({
                'tooltip': {'trigger': 'item'},
                'series': [
                    {
                        'type': 'pie',
                        'radius': ['40%', '70%'],
                        'data': pie_data,
                    }
                ],
            }).classes("w-full h-64")

        # Gráfico de pizza 2
        with ui.card():
            ui.label("Gráfico de X (Pizza 2)").classes("text-lg font-bold mb-2")
            ui.echart({
                'tooltip': {'trigger': 'item'},
                'series': [
                    {
                        'type': 'pie',
                        'radius': ['40%', '70%'],
                        'data': pie_data,
                    }
                ],
            }).classes("w-full h-64")

    ui.label("Despesas").classes("text-xl mt-6 mb-4")

    columns = [
      {'name': 'ID', 'label': 'Id', 'field': 'ID', 'required': True, 'align': 'left'},
      {'name': 'Nome', 'label': 'Nome', 'field': 'Nome'},
      {'name': 'Valor', 'label': 'Valor', 'field': 'Valor'},
    ]
    ui.table(columns=columns, rows=expenses, row_key='name').classes("w-full")
