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
        with ui.element('div').classes('flex bg-white flex-col w-full -m-4 p-8 gap-8'):
            with ui.row().classes("justify-between w-full items-center"):
                ui.label("Despesas Relacionadas aos Consertos").classes("text-2xl font-bold")
                ui.button(icon='person', on_click=lambda: ui.notify("Perfil clicado!"))

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

            with ui.element('div').classes("grid grid-cols-1 w-full gap-6"):
                for grafico in graficos:
                    grafico_path = os.path.join(OUTPUT_DIR, grafico['image'])
                    if os.path.exists(grafico_path):
                        with ui.card().classes("flex flex-col items-center gap-4 bg-[#FAFAFA] rounded-xl p-4 shadow-none"):
                            ui.label(grafico['title']).classes("text-lg font-semibold")
                            ui.image(f"data:image/png;base64,{img_to_base64(grafico_path)}").classes("w-full h-64 object-contain")
                    else:
                        ui.notify(f"Gráfico {grafico['image']} não encontrado.", type='error')

        # Navegação
        with ui.left_drawer().props("width=260").classes("bg-[#FBFBFB] flex flex-col gap-4 border-r border-[#E4E4E7]") as drawer:
            ui.label('Logo').classes('text-3xl block mb-8 font-bold')
            
            with ui.row().classes('flex gap-2 items-center'):
                ui.icon('home').classes('w-4 h-4 text-[#71717A]')
                ui.link("Dashboard", "/").classes("text-[#71717A] no-underline font-medium")

            with ui.row().classes('flex gap-2 items-center'):
                ui.icon('money').classes('w-4 h-4 text-[#18181B]')
                ui.link("Despesas", "/expenses").classes("text-[#18181B] no-underline font-medium")

    # Registrar a página
    expenses_page()
