# dashboard.py

from nicegui import ui
import base64
import os
import pandas as pd

def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def setup_dashboard(df_unificado, tecnico_count_df):
    @ui.page("/")
    def dashboard_page():
        with ui.element('div').classes('flex bg-white flex-col w-full -m-4 p-8 gap-8'):
            with ui.row().classes("justify-between w-full items-center"):
                ui.label("Dashboard de Análise de Consertos").classes("text-2xl font-bold")
                ui.button(icon='person', on_click=lambda: ui.notify("Perfil clicado!"))

            OUTPUT_DIR = os.path.join(os.getcwd(), 'data', 'outputs')

            # Função para obter o caminho completo do gráfico
            def get_graph_path(filename):
                return os.path.join(OUTPUT_DIR, filename)

            graficos = [
                {
                    'title': "Distribuição do Tempo de Conserto (Boxplot)",
                    'image': "boxplot_tempo_conserto.png"
                },
                {
                    'title': "Evolução do Tempo Médio de Conserto",
                    'image': "linha_tempo_medio_conserto.png"
                },
                {
                    'title': "Taxa de Sucesso para Conserto",
                    'image': "pizza_taxa_sucesso.png"
                },
                {
                    'title': "Número de Aparelhos Recebidos ao Longo do Tempo",
                    'image': "linha_aparelhos_recebidos.png"
                },
                {
                    'title': "Número de Aparelhos Recebidos por Marca",
                    'image': "barra_aparelhos_por_marca.png"
                },
                {
                    'title': "Número de Aparelhos Recebidos por Tipo de Aparelho",
                    'image': "barra_aparelhos_por_tipo.png"
                },
                {
                    'title': "Consertos por Funcionário",
                    'image': "grafico_consertos_tecnicos.png"
                }
            ]

            with ui.element('div').classes("grid grid-cols-1 w-full gap-6"):
                for grafico in graficos:
                    grafico_path = get_graph_path(grafico['image'])
                    if os.path.exists(grafico_path):
                        with ui.card().classes("flex flex-col items-center gap-4 bg-[#FAFAFA] rounded-xl p-4 shadow-none"):
                            ui.label(grafico['title']).classes("text-lg font-semibold")
                            ui.image(f"data:image/png;base64,{img_to_base64(grafico_path)}").classes("w-full h-64 object-contain")
                    else:
                        ui.notify(f"Gráfico {grafico['image']} não encontrado.", type='error')

            with ui.element('div').classes('flex flex-col gap-4'):
                ui.label("Tabela de Técnicos").classes("text-xl font-bold")
                columns = [
                    {'name': 'TECNICO', 'label': 'Técnico', 'field': 'TECNICO', 'required': True, 'align': 'left'},
                    {'name': 'QUANTIDADE', 'label': 'Quantidade de Consertos', 'field': 'QUANTIDADE'},
                    {'name': 'CONCLUIDOS', 'label': 'Consertos Concluídos', 'field': 'CONCLUIDOS'},
                    {'name': 'NAO_CONCLUIDOS', 'label': 'Consertos Não Concluídos', 'field': 'NAO_CONCLUIDOS'},
                ]
                ui.table(columns=columns, rows=tecnico_count_df.to_dict('records'), row_key='TECNICO', pagination=10).classes("w-full p-4")

        with ui.left_drawer().props("width=260").classes("bg-[#FBFBFB] flex flex-col gap-4 border-r border-[#E4E4E7]") as drawer:
            ui.label('Logo').classes('text-3xl block mb-8 font-bold')
            
            with ui.row().classes('flex gap-2 items-center'):
                ui.icon('home').classes('w-4 h-4')
                ui.link("Dashboard", "/").classes("text-[#18181B] no-underline font-medium")

            with ui.row().classes('flex gap-2 items-center'):
                ui.icon('money').classes('w-4 h-4 text-[#71717A]')
                ui.link("Despesas", "/expenses").classes("text-[#71717A] no-underline font-medium")

    # Registrar a página
    dashboard_page()
