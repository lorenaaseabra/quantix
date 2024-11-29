# dashboard.py

from nicegui import ui
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

# Função para converter imagens PNG em string base64
def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def setup_dashboard(df_unificado, tecnico_count_df):
    # Funções para obter os gráficos já salvos
    def get_boxplot():
        return img_to_base64('boxplot_tempo_conserto.png')

    def get_linha_tempo_medio():
        return img_to_base64('linha_tempo_medio_conserto.png')

    def get_pizza_taxa_sucesso():
        return img_to_base64('pizza_taxa_sucesso.png')

    @ui.page("/")
    def dashboard_page():
        with ui.row().classes("gap-4 items-center"):
            ui.label("Dashboard de Análise de Consertos").classes("text-lg font-bold")

        # Gráficos
        with ui.row().classes("w-full grid grid-cols-2 gap-4"):
            # Gráfico de Boxplot
            with ui.card():
                ui.label("Distribuição do Tempo de Conserto (Boxplot)").classes("text-lg font-bold mb-2")
                ui.image(f"data:image/png;base64,{get_boxplot()}").classes("w-full h-64")

            # Gráfico de Linha
            with ui.card():
                ui.label("Evolução do Tempo Médio de Conserto").classes("text-lg font-bold mb-2")
                ui.image(f"data:image/png;base64,{get_linha_tempo_medio()}").classes("w-full h-64")

            # Gráfico de Pizza
            with ui.card():
                ui.label("Taxa de Sucesso para Conserto").classes("text-lg font-bold mb-2")
                ui.image(f"data:image/png;base64,{get_pizza_taxa_sucesso()}").classes("w-full h-64")

            # Gráfico de Aparelhos Recebidos
            with ui.card():
                ui.label("Número de Aparelhos Recebidos ao Longo do Tempo").classes("text-lg font-bold mb-2")
                ui.image(f"data:image/png;base64,{img_to_base64('linha_aparelhos_recebidos.png')}").classes("w-full h-64")

            # Gráfico de Aparelhos por Marca (se existir)
            if 'MARCA' in df_unificado.columns:
                with ui.card():
                    ui.label("Número de Aparelhos Recebidos por Marca").classes("text-lg font-bold mb-2")
                    ui.image(f"data:image/png;base64,{img_to_base64('barra_aparelhos_por_marca.png')}").classes("w-full h-64")

            # Gráfico de Aparelhos por Tipo (se existir)
            if 'APARELHO' in df_unificado.columns:
                with ui.card():
                    ui.label("Número de Aparelhos Recebidos por Tipo de Aparelho").classes("text-lg font-bold mb-2")
                    ui.image(f"data:image/png;base64,{img_to_base64('barra_aparelhos_por_tipo.png')}").classes("w-full h-64")

        # Tabela de Técnicos
        ui.label("Tabela de Técnicos").classes("text-xl mt-6 mb-4")
        columns = [
            {'name': 'TECNICO', 'label': 'Técnico', 'field': 'TECNICO', 'required': True, 'align': 'left'},
            {'name': 'QUANTIDADE', 'label': 'Quantidade de Consertos', 'field': 'QUANTIDADE'},
            {'name': 'CONCLUIDOS', 'label': 'Consertos Concluídos', 'field': 'CONCLUIDOS'},
            {'name': 'NAO_CONCLUIDOS', 'label': 'Consertos Não Concluídos', 'field': 'NAO_CONCLUIDOS'},
        ]
        ui.table(columns=columns, rows=tecnico_count_df.to_dict('records'), row_key='TECNICO').classes("w-full")

        # Navegação
        with ui.left_drawer() as drawer:
            ui.link("Dashboard", "/").classes("block py-2")
            ui.link("Despesas", "/expenses").classes("block py-2")
            ui.link("Livros", "/books").classes("block py-2")

    # Registrar a página
    dashboard_page()
