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
        with ui.row().classes("gap-4 items-center p-4"):
            ui.label("Dashboard de Análise de Consertos").classes("text-2xl font-bold")

        # Diretório de outputs
        OUTPUT_DIR = os.path.join(os.getcwd(), 'data', 'outputs')

        # Função para obter o caminho completo do gráfico
        def get_graph_path(filename):
            return os.path.join(OUTPUT_DIR, filename)

        # Lista de gráficos para o dashboard
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

        with ui.grid().classes("w-full gap-4 p-4"):
            for grafico in graficos:
                grafico_path = get_graph_path(grafico['image'])
                if os.path.exists(grafico_path):
                    with ui.card().classes("flex flex-col items-center p-4"):
                        ui.label(grafico['title']).classes("text-lg font-semibold mb-2")
                        ui.image(f"data:image/png;base64,{img_to_base64(grafico_path)}").classes("w-full h-64 object-contain")
                else:
                    ui.notify(f"Gráfico {grafico['image']} não encontrado.", type='error')

        # Tabela de Técnicos
        ui.label("Tabela de Técnicos").classes("text-xl mt-6 mb-4 px-4")
        columns = [
            {'name': 'TECNICO', 'label': 'Técnico', 'field': 'TECNICO', 'required': True, 'align': 'left'},
            {'name': 'QUANTIDADE', 'label': 'Quantidade de Consertos', 'field': 'QUANTIDADE'},
            {'name': 'CONCLUIDOS', 'label': 'Consertos Concluídos', 'field': 'CONCLUIDOS'},
            {'name': 'NAO_CONCLUIDOS', 'label': 'Consertos Não Concluídos', 'field': 'NAO_CONCLUIDOS'},
        ]
        ui.table(columns=columns, rows=tecnico_count_df.to_dict('records'), row_key='TECNICO').classes("w-full p-4")

        # Navegação
        with ui.left_drawer().classes("p-4"):
            ui.link("Dashboard", "/").classes("block py-2 text-blue-600")
            ui.link("Despesas", "/expenses").classes("block py-2 text-blue-600")

    # Registrar a página
    dashboard_page()
