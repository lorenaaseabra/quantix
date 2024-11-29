# expenses.py

from nicegui import ui
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def setup_expenses(df_unificado, tecnico_count_df):
    @ui.page("/expenses")
    def expenses_page():
        # Cabeçalho
        with ui.row().classes("justify-between w-full items-center mb-4"):
            ui.label("Logo").classes("text-lg font-bold")
            ui.button("Perfil", on_click=lambda: ui.notify("Perfil clicado!"))

        ui.label("Despesas Relacionadas aos Consertos").classes("text-xl mb-4")

        # Gráficos
        with ui.row().classes("w-full grid grid-cols-2 gap-4"):
            # Gráfico de Consertos por Técnico
            with ui.card():
                ui.label("Consertos por Técnico").classes("text-lg font-bold mb-2")
                # Gerar gráfico de barras utilizando matplotlib
                plt.figure(figsize=(10, 6))
                tecnico_count_df.plot(kind='bar', x='TECNICO', y='QUANTIDADE', color='skyblue')
                plt.title('Número de Consertos por Técnico')
                plt.xlabel('Técnico')
                plt.ylabel('Quantidade de Consertos')
                plt.xticks(rotation=90)
                plt.tight_layout()
                # Salvar o gráfico em memória
                buf = io.BytesIO()
                plt.savefig(buf, format="png")
                buf.seek(0)
                img_str = base64.b64encode(buf.read()).decode("utf-8")
                buf.close()
                plt.close()
                # Exibir a imagem
                ui.image(f"data:image/png;base64,{img_str}").classes("w-full h-64")

            # Gráfico de Taxa de Sucesso (Reutilizando do dashboard)
            with ui.card():
                ui.label("Taxa de Sucesso para Conserto").classes("text-lg font-bold mb-2")
                ui.image(f"data:image/png;base64,{img_to_base64('pizza_taxa_sucesso.png')}").classes("w-full h-64")

            # Gráfico de Aparelhos Recebidos (Reutilizando do dashboard)
            with ui.card():
                ui.label("Aparelhos Recebidos por Mês").classes("text-lg font-bold mb-2")
                ui.image(f"data:image/png;base64,{img_to_base64('linha_aparelhos_recebidos.png')}").classes("w-full h-64")

            # Gráfico de Tempo de Conserto (Boxplot) (Reutilizando do dashboard)
            with ui.card():
                ui.label("Distribuição do Tempo de Conserto").classes("text-lg font-bold mb-2")
                ui.image(f"data:image/png;base64,{img_to_base64('boxplot_tempo_conserto.png')}").classes("w-full h-64")

        # Tabela de Despesas (Exemplo Fictício)
        ui.label("Despesas").classes("text-xl mt-6 mb-4")
        columns = [
            {'name': 'ID', 'label': 'Id', 'field': 'ID', 'required': True, 'align': 'left'},
            {'name': 'Nome', 'label': 'Nome', 'field': 'Nome'},
            {'name': 'Valor', 'label': 'Valor', 'field': 'Valor'},
        ]
        expenses = [
            {"ID": 1, "Nome": "Despesa 1", "Valor": "R$3000,00"},
            {"ID": 2, "Nome": "Despesa 2", "Valor": "R$2500,00"},
            {"ID": 3, "Nome": "Despesa 3", "Valor": "R$1500,00"},
            {"ID": 4, "Nome": "Despesa 4", "Valor": "R$1000,00"},
        ]
        ui.table(columns=columns, rows=expenses, row_key='ID').classes("w-full")

        # Navegação
        with ui.left_drawer() as drawer:
            ui.link("Dashboard", "/").classes("block py-2")
            ui.link("Despesas", "/expenses").classes("block py-2")
            ui.link("Livros", "/books").classes("block py-2")

    # Registrar a página
    expenses_page()
