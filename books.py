# books.py

from nicegui import ui
from random import randint, random
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def setup_books(df_unificado, tecnico_count_df):
    @ui.page("/books")
    def books_page():
        # Cabeçalho
        with ui.row().classes("justify-between w-full items-center mb-4"):
            ui.label("Logo").classes("text-lg font-bold")
            ui.button("Perfil", on_click=lambda: ui.notify("Perfil clicado!"))

        ui.label("Informações Gerais dos Livros").classes("text-xl mb-4")

        # Gráficos
        with ui.row().classes("w-full grid grid-cols-2 gap-4"):
            # Gráfico de Barras (Exemplo Fictício)
            with ui.card():
                ui.label("Gráfico de Barras").classes("text-lg font-bold mb-2")
                # Dados fictícios de exemplo
                months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                bar_data = [randint(10, 100) for _ in months]
                plt.figure(figsize=(12, 6))
                plt.bar(months, bar_data, color='skyblue')
                plt.title('Exemplo de Gráfico de Barras')
                plt.xlabel('Mês')
                plt.ylabel('Quantidade')
                plt.xticks(rotation=45)
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

            # Gráfico de Linha (Exemplo Fictício)
            with ui.card():
                ui.label("Gráfico de Linha").classes("text-lg font-bold mb-2")
                # Dados fictícios de exemplo
                line_data = [randint(50, 150) for _ in months]
                plt.figure(figsize=(12, 6))
                plt.plot(months, line_data, marker='o', linestyle='-', color='lightcoral')
                plt.title('Exemplo de Gráfico de Linha')
                plt.xlabel('Mês')
                plt.ylabel('Valor')
                plt.xticks(rotation=45)
                plt.grid(True)
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

            # Gráfico de Barras Agrupadas (Exemplo Fictício)
            with ui.card().classes("col-span-2"):
                ui.label("Gráfico de Barras Agrupadas").classes("text-lg font-bold mb-2")
                # Dados fictícios de exemplo
                grouped_bar_data = {
                    "A": [randint(20, 100) for _ in range(5)],
                    "B": [randint(10, 80) for _ in range(5)],
                }
                grupos = [f"Grupo {i}" for i in range(1, 6)]
                x = range(len(grupos))
                width = 0.35

                plt.figure(figsize=(12, 6))
                plt.bar([p - width/2 for p in x], grouped_bar_data["A"], width=width, label='A', color='skyblue')
                plt.bar([p + width/2 for p in x], grouped_bar_data["B"], width=width, label='B', color='lightcoral')
                plt.title('Exemplo de Gráfico de Barras Agrupadas')
                plt.xlabel('Grupo')
                plt.ylabel('Quantidade')
                plt.xticks(x, grupos, rotation=45)
                plt.legend()
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

        # Tabela de Livros (Exemplo Fictício)
        ui.label("Livros").classes("text-xl mt-6 mb-4")
        columns = [
            {'name': 'ID', 'label': 'Id', 'field': 'ID', 'required': True, 'align': 'left'},
            {'name': 'Nome', 'label': 'Nome', 'field': 'Nome'},
            {'name': 'Valor', 'label': 'Valor', 'field': 'Valor'},
        ]
        books = [
            {"ID": 1, "Nome": "Livro 1", "Valor": "R$3000,00"},
            {"ID": 2, "Nome": "Livro 2", "Valor": "R$2500,00"},
            {"ID": 3, "Nome": "Livro 3", "Valor": "R$1500,00"},
            {"ID": 4, "Nome": "Livro 4", "Valor": "R$1000,00"},
        ]
        ui.table(columns=columns, rows=books, row_key='ID').classes("w-full")

        # Navegação
        with ui.left_drawer() as drawer:
            ui.link("Dashboard", "/").classes("block py-2")
            ui.link("Despesas", "/expenses").classes("block py-2")
            ui.link("Livros", "/books").classes("block py-2")

    # Registrar a página
    books_page()
