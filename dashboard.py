from nicegui import ui
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

# Carregar os dados
df_unificado = pd.read_csv('data\Dados_Unificados.csv')  # Carregar o CSV unificado

# Função para gerar os gráficos
def create_plot_1():
    # Gráfico de Boxplot
    plt.figure(figsize=(10, 6))
    plt.boxplot(df_unificado['TEMPO_CONSERTO'].dropna(), vert=False, patch_artist=True, boxprops=dict(facecolor='skyblue'))
    plt.title('Distribuição do Tempo de Conserto (em dias)')
    plt.xlabel('Tempo de Conserto (dias)')
    plt.tight_layout()
    
    # Salvar o gráfico em memória
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    
    return img_str

def create_plot_2():
    # Gráfico de Linha: Evolução do Tempo Médio de Conserto
    tempo_medio_por_mes = df_unificado.groupby('MES_ANO')['TEMPO_CONSERTO'].mean().reset_index()
    
    plt.figure(figsize=(12, 6))
    plt.plot(tempo_medio_por_mes['MES_ANO'], tempo_medio_por_mes['TEMPO_CONSERTO'], marker='o', linestyle='-', color='skyblue')
    plt.title('Evolução do Tempo Médio de Conserto')
    plt.xlabel('Mês/Ano')
    plt.ylabel('Tempo Médio de Conserto (dias)')
    plt.xticks(rotation=90)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Salvar o gráfico em memória
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    
    return img_str

def create_plot_3():
    # Gráfico de Pizza: Taxa de Sucesso para Conserto
    taxa_sucesso = df_unificado['CONSERTADO'].value_counts()
    
    plt.figure(figsize=(8, 8))
    taxa_sucesso.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightcoral'])
    plt.title('Taxa de Sucesso para Conserto')
    plt.ylabel('')
    plt.tight_layout()
    
    # Salvar o gráfico em memória
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    
    return img_str

# Página principal
@ui.page("/")
def dashboard():
    with ui.row().classes("gap-4 items-center"):
        ui.label("Dashboard de Análise de Consertos").classes("text-lg font-bold")

    # Gráficos
    with ui.row().classes("w-full grid grid-cols-2 gap-4"):
        # Gráfico de Boxplot
        with ui.card():
            ui.label("Distribuição do Tempo de Conserto (Boxplot)").classes("text-lg font-bold mb-2")
            ui.image(f"data:image/png;base64,{create_plot_1()}").classes("w-full h-64")
        
        # Gráfico de Linha
        with ui.card():
            ui.label("Evolução do Tempo Médio de Conserto").classes("text-lg font-bold mb-2")
            ui.image(f"data:image/png;base64,{create_plot_2()}").classes("w-full h-64")
        
        # Gráfico de Pizza
        with ui.card():
            ui.label("Taxa de Sucesso para Conserto").classes("text-lg font-bold mb-2")
            ui.image(f"data:image/png;base64,{create_plot_3()}").classes("w-full h-64")

    # Navegação
    with ui.left_drawer() as drawer:
        ui.link("Dashboard", "/").classes("block py-2")

# Iniciar o servidor NiceGUI
ui.run(title="Dashboard Análise de Consertos", port=8080)
