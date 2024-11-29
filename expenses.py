# expenses.py

from nicegui import ui
import base64
import os

def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def setup_expenses(df_unificado, tecnico_count_df):
    @ui.page("/expenses")
    def expenses_page():
        with ui.row().classes("justify-between w-full items-center mb-4 p-4"):
            ui.label("Logo").classes("text-lg font-bold")
            ui.button("Perfil", on_click=lambda: ui.notify("Perfil clicado!"))

        ui.label("Despesas Relacionadas aos Consertos").classes("text-2xl mb-4 p-4")

        # Diretório de outputs
        OUTPUT_DIR = os.path.join(os.getcwd(), 'data', 'outputs')

        # Lista de gráficos para despesas
        graficos = [
            {
                'title': "Despesas Mensais por Categoria (Top 10)",
                'image': "despesas_mensais_top10.png"
            },
            {
                'title': "Despesas por Categoria",
                'image': "despesas_por_categoria.png"
            },
            {
                'title': "Distribuição das Formas de Pagamento",
                'image': "distribuicao_formas_pagamento.png"
            },
            {
                'title': "Proporção de Situação de Pagamento",
                'image': "proporcao_situacao_pagamento.png"
            }
        ]

        with ui.grid().classes("w-full gap-4 p-4"):
            for grafico in graficos:
                grafico_path = os.path.join(OUTPUT_DIR, grafico['image'])
                if os.path.exists(grafico_path):
                    with ui.card().classes("flex flex-col items-center p-4"):
                        ui.label(grafico['title']).classes("text-lg font-semibold mb-2")
                        ui.image(f"data:image/png;base64,{img_to_base64(grafico_path)}").classes("w-full h-64 object-contain")
                else:
                    ui.notify(f"Gráfico {grafico['image']} não encontrado.", type='error')

        # Navegação
        with ui.left_drawer().classes("p-4"):
            ui.link("Dashboard", "/").classes("block py-2 text-blue-600")
            ui.link("Despesas", "/expenses").classes("block py-2 text-blue-600")

    # Registrar a página
    expenses_page()
