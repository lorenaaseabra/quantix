from nicegui import ui
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import os

# Função para converter imagens para base64
def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Função para gerar gráficos e convertê-los para base64
def plot_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    plt.close(fig)
    return img_str

def setup_expenses(df_unificado, tecnico_count_df):
    @ui.page("/expenses")
    def expenses_page():
        # Cabeçalho
        with ui.row().classes("justify-between w-full items-center mb-4"):
            ui.label("Logo").classes("text-lg font-bold")
            ui.button("Perfil", on_click=lambda: ui.notify("Perfil clicado!"))

        ui.label("Despesas Relacionadas aos Consertos").classes("text-xl mb-4")

        # Leitura do arquivo de despesas
        file_path = os.path.join('data', 'Tratamento dos dados - 2021.csv')
        dados_empresa = pd.read_csv(file_path)

        # Processamento de Dados
        dados_empresa['Valor'] = dados_empresa['Valor'].replace('[R$\s]', '', regex=True).str.replace(',', '').astype(float)
        dados_empresa['Forma de Pagamento'] = dados_empresa['Forma de Pagamento'].fillna('Forma de Pagamento nao definido')
        dados_empresa['Parcela'] = dados_empresa['Parcela'].fillna('1/1')

        meses_dict = {
            'Janeiro': '01', 'Fevereiro': '02', 'Março': '03', 'Abril': '04',
            'Maio': '05', 'Junho': '06', 'Julho': '07', 'Agosto': '08',
            'Setembro': '09', 'Outubro': '10', 'Novembro': '11', 'Dezembro': '12'
        }

        dados_empresa['Mês_Num'] = dados_empresa['Mês'].map(meses_dict)
        dados_empresa['Data'] = pd.to_datetime(
            dados_empresa['Dia'].astype(str) + '/' + dados_empresa['Mês_Num'] + '/2021',
            format='%d/%m/%Y',
            errors='coerce'
        )

        # Total de despesas por categoria
        custo_categoria = dados_empresa.groupby('Categoria')['Valor'].sum()

        # Gráfico de barras: Despesas por categoria
        fig1 = plt.figure(figsize=(10, 5))
        custo_categoria.plot(kind='bar')
        plt.title('Despesas por Categoria')
        plt.xlabel('Categoria')
        plt.ylabel('Custo Total (R$)')
        despesa_categoria_base64 = plot_to_base64(fig1)

        # Gráfico de pizza: Distribuição das formas de pagamento
        formas_pagamento = dados_empresa['Forma de Pagamento'].value_counts()
        fig2 = plt.figure(figsize=(10, 5))
        formas_pagamento.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Distribuição das Formas de Pagamento')
        formas_pagamento_base64 = plot_to_base64(fig2)

        # Gráfico de linhas: Top 10 categorias de despesas
        valor_total_por_categoria = dados_empresa.groupby('Categoria')['Valor'].sum().sort_values(ascending=False)
        top_10_categorias = valor_total_por_categoria.head(10).index
        dados_filtrados = dados_empresa[dados_empresa['Categoria'].isin(top_10_categorias)]

        fig3 = plt.figure(figsize=(12, 6))
        for categoria in top_10_categorias:
            gastos_categoria = dados_filtrados[dados_filtrados['Categoria'] == categoria]
            gastos_categoria_mensal = gastos_categoria.groupby(dados_filtrados['Data'].dt.month)['Valor'].sum()
            plt.plot(gastos_categoria_mensal.index, gastos_categoria_mensal.values, marker='o', label=categoria)
        plt.title('Despesas Mensais por Categoria (Top 10)')
        plt.xlabel('Mês')
        plt.ylabel('Total de Despesas (R$)')
        plt.legend(loc='best', fontsize=8)
        despesa_categoria_mensal_base64 = plot_to_base64(fig3)

        # Gráfico de barras: Situação de pagamento
        dados_empresa['Situação'] = dados_empresa['Situação'].fillna('Não Pago')
        situacao_proporcao = dados_empresa['Situação'].value_counts()
        fig4 = plt.figure(figsize=(8, 5))
        situacao_proporcao.plot(kind='bar', color='skyblue')
        plt.title('Proporção de Situação de Pagamento')
        plt.xlabel('Situação')
        plt.ylabel('Quantidade de Transações')
        situacao_pagamento_base64 = plot_to_base64(fig4)

        # Exibir gráficos na página
        with ui.row().classes("w-full grid grid-cols-2 gap-4"):
            with ui.card():
                ui.label("Despesas por Categoria").classes("text-lg font-bold mb-2")
                ui.image(f"data:image/png;base64,{despesa_categoria_base64}").classes("w-full h-64")

            with ui.card():
                ui.label("Formas de Pagamento").classes("text-lg font-bold mb-2")
                ui.image(f"data:image/png;base64,{formas_pagamento_base64}").classes("w-full h-64")

            with ui.card():
                ui.label("Despesas Mensais por Categoria (Top 10)").classes("text-lg font-bold mb-2")
                ui.image(f"data:image/png;base64,{despesa_categoria_mensal_base64}").classes("w-full h-64")

            with ui.card():
                ui.label("Situação de Pagamento").classes("text-lg font-bold mb-2")
                ui.image(f"data:image/png;base64,{situacao_pagamento_base64}").classes("w-full h-64")

        # Navegação
        with ui.left_drawer() as drawer:
            ui.link("Dashboard", "/").classes("block py-2")
            ui.link("Despesas", "/expenses").classes("block py-2")

    # Registrar a página
    expenses_page()
