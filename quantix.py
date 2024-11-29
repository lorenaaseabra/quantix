# quantix.py

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Arial'
import re
import os



def process_data():
    
    # Definir o diretório de saída para os gráficos
    BASE_DIR = os.getcwd()
    OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'outputs')
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # Criar a pasta, se não existir

    # Salvar os gráficos no diretório de saída
    plt.savefig(os.path.join(OUTPUT_DIR, 'grafico_tempo_conserto.png'))
    
    # Caminho para os arquivos CSV
    caminho_dados = 'data/'

    # Leitura dos arquivos CSV
    df2018 = pd.read_csv(f'{caminho_dados}Dados_Tratados_Normalizados_2018 - Dados_Normalizados_Eceel_Tec.csv')
    df2020 = pd.read_csv(f'{caminho_dados}Dados_Tratados_Normalizados_2020 - Dados_Normalizados_Eceel_Tec_2020.csv')
    df2021 = pd.read_csv(f'{caminho_dados}Dados_Normalizados_ECEEL_TEC_2021 - Dados_Normalizados_ECEEL_TEC_2021.csv')
    df2022 = pd.read_csv(f'{caminho_dados}Dados_Tratados_Normalizados_2022 - Dados_Tratados_Normalizados_2022.csv')
    df2023 = pd.read_csv(f'{caminho_dados}Dados_Tratados_ECEEL_TEC_2023 - Dados_Tratados_ECEEL_TEC_2023.csv')
    df2024 = pd.read_csv(f'{caminho_dados}Dados_Tratados_e_Normalizados_ECEEL_TEC_2024 - Dados_Tratados_e_Normalizados_ECEEL_TEC.csv')

    # **Tratamento das planilhas**

    ## Unificação das tabelas

    # Remover a coluna 'ORDEM' de 2022, caso ela exista
    if 'ORDEM' in df2022.columns:
        df2022 = df2022.drop(columns=['ORDEM'])

    # Renomear as colunas para garantir consistência nos nomes
    rename_columns = {
        'CONSERTADO?': 'CONSERTADO',           # Unificar a coluna 'CONSERTADO?' para 'CONSERTADO'
        'PEÇA RECEBIDA': 'PECA_RECEBIDA',      # Unificar a coluna 'PEÇA RECEBIDA' para 'PECA_RECEBIDA'
        'SAÍDA': 'SAIDA',                      # Unificar a coluna 'SAÍDA' para 'SAIDA'
        'TIPO_DE_AT': 'TIPO DE AT.'            # Unificar a coluna 'TIPO_DE_AT' para 'TIPO DE AT.'
    }

    # Renomear as colunas nos DataFrames
    for df in [df2018, df2020, df2021, df2022, df2023, df2024]:
        df.rename(columns=rename_columns, inplace=True)

    # Adicionar a coluna 'TECNICO' com valores null (ou 0) nos DataFrames que não possuem essa coluna
    for df in [df2018, df2020, df2021, df2022, df2023, df2024]:
        if 'TECNICO' not in df.columns:
            df['TECNICO'] = None

    # Concatenar todos os DataFrames
    df_unificado = pd.concat([df2018, df2020, df2021, df2022, df2023, df2024], ignore_index=True)

    # Remover a coluna 'Dados_Tratados_e_Normalizados_ECEEL_TEC' se existir
    if 'Dados_Tratados_e_Normalizados_ECEEL_TEC' in df_unificado.columns:
        df_unificado = df_unificado.drop(columns=['Dados_Tratados_e_Normalizados_ECEEL_TEC'])

    # Padronizar a coluna 'CONSERTADO'
    df_unificado['CONSERTADO'] = df_unificado['CONSERTADO'].astype(str).str.strip().str.lower()

    # Substituir valores incorretos por "sim"
    valores_sim = ['sm', 'si,', 'sim.', 'siim']
    df_unificado['CONSERTADO'] = df_unificado['CONSERTADO'].replace(valores_sim, 'sim')

    # Remover valores indesejados
    valores_a_remover = ['0', '19/02/2021']
    df_unificado = df_unificado[~df_unificado['CONSERTADO'].isin(valores_a_remover)]

    # Garantir que a coluna 'TECNICO' não tenha valores nulos ou espaços extras
    df_unificado['TECNICO'] = df_unificado['TECNICO'].fillna('0').astype(str).str.strip()

    # Substituir diferentes separadores por um único separador "/"
    df_unificado['TECNICO'] = (
        df_unificado['TECNICO']
        .str.replace(r'\s+e\s+', '/', regex=True)    # Substituir " e " por "/"
        .str.replace(r'\s+E\s+', '/', regex=True)    # Substituir " E " por "/"
        .str.replace(r'\s*,\s*', '/', regex=True)    # Substituir "," por "/"
        .str.replace(r'\s*-\s*', '/', regex=True)    # Substituir "-" por "/"
    )

    # Transformar todos os nomes em maiúsculas
    df_unificado['TECNICO'] = df_unificado['TECNICO'].str.upper()

    # Separar os técnicos combinados e expandir a lista em novas linhas
    df_unificado_expanded = df_unificado.assign(TECNICO=df_unificado['TECNICO'].str.split('/')).explode('TECNICO')

    # Remover espaços extras ao redor dos nomes
    df_unificado_expanded['TECNICO'] = df_unificado_expanded['TECNICO'].str.strip()

    # Contar a ocorrência de cada técnico
    tecnico_count = df_unificado_expanded['TECNICO'].value_counts()

    # Converter a contagem para um DataFrame
    tecnico_count_df = tecnico_count.reset_index()
    tecnico_count_df.columns = ['TECNICO', 'QUANTIDADE']

    # Filtrar técnicos válidos (remover valores vazios ou "0")
    tecnico_count_df = tecnico_count_df[(tecnico_count_df['TECNICO'] != '') & (tecnico_count_df['TECNICO'] != '0')]

    # Contar consertos "Sim" e "Não" para cada técnico
    consertos_tecnico = (
        df_unificado_expanded.groupby(['TECNICO', 'CONSERTADO'])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    # Renomear colunas para clareza
    consertos_tecnico = consertos_tecnico.rename(columns={'sim': 'CONCLUIDOS', 'não': 'NAO_CONCLUIDOS'})

    # Unir os dados ao tecnico_count_df
    tecnico_count_df = pd.merge(tecnico_count_df, consertos_tecnico, on='TECNICO', how='left')

    # Salvar o DataFrame de contagem de técnicos em um arquivo CSV
    tecnico_count_df.to_csv('tecnico_count.csv', index=False)

    # Lista de colunas de datas
    colunas_datas = ['PECA_RECEBIDA', 'SAIDA', 'PRONTO', 'DATA']

    # Substituir valores problemáticos ('0', 'null', '00/00/0000') por NaN para todas as colunas de data
    for coluna in colunas_datas:
        if coluna in df_unificado.columns:
            df_unificado[coluna] = df_unificado[coluna].replace(['0', 'null', '00/00/0000'], pd.NA)

    # Função para verificar o formato de datas e corrigir para o padrão dd/mm/aaaa
    def corrigir_data(data):
        if pd.isna(data):
            return pd.NA
        data = str(data).strip()  # Garantir que o valor seja uma string e remover espaços
        if re.match(r'^\d{2}-\d{2}-\d{4}$', data):
            # Converte dd-mm-aaaa para dd/mm/aaaa
            return data.replace('-', '/')
        elif re.match(r'^\d{2}/\d{2}/\d{4}$', data):
            # Mantém o formato dd/mm/aaaa
            return data
        return pd.NA  # Retorna NaN para valores fora do padrão

    # Corrigir datas em cada coluna
    for coluna in colunas_datas:
        if coluna in df_unificado.columns:
            df_unificado[coluna] = df_unificado[coluna].apply(corrigir_data)

    # Remover apenas as linhas que ainda possuem algum valor inválido em todas as colunas de datas
    df_unificado = df_unificado.dropna(subset=colunas_datas, how='all')

    # Verificar se há datas inválidas restantes após a correção
    linhas_invalidas = {}
    for coluna in colunas_datas:
        if coluna in df_unificado.columns:
            linhas_invalidas[coluna] = df_unificado[df_unificado[coluna].isna()]

    # **Calcular 'TEMPO_CONSERTO'**

    # Garantir que as colunas de datas estejam no formato datetime
    df_unificado['PECA_RECEBIDA'] = pd.to_datetime(df_unificado['PECA_RECEBIDA'], format='%d/%m/%Y', errors='coerce')
    df_unificado['PRONTO'] = pd.to_datetime(df_unificado['PRONTO'], format='%d/%m/%Y', errors='coerce')

    # Remover linhas com datas inválidas após a conversão
    df_unificado = df_unificado.dropna(subset=['PECA_RECEBIDA', 'PRONTO'])

    # Calcular o tempo de conserto em dias
    df_unificado['TEMPO_CONSERTO'] = (df_unificado['PRONTO'] - df_unificado['PECA_RECEBIDA']).dt.days

    # Identificar e remover entradas com 'TEMPO_CONSERTO' negativo
    negativos = df_unificado[df_unificado['TEMPO_CONSERTO'] < 0]
    if not negativos.empty:
        # Opcional: Remover essas entradas
        df_unificado = df_unificado[df_unificado['TEMPO_CONSERTO'] >= 0]

    # Criar coluna de mês/ano para agrupamento
    df_unificado['MES_ANO'] = df_unificado['PECA_RECEBIDA'].dt.to_period('M').astype(str)

    # Remover valores de MES_ANO incorretos (exemplo: '2025-05')
    valores_incorretos = ['2025-05']
    df_unificado = df_unificado[~df_unificado['MES_ANO'].isin(valores_incorretos)]

    # **Salvar o DataFrame Unificado após criar 'TEMPO_CONSERTO'**

    df_unificado.to_csv('Dados_Unificados.csv', index=False)

    # **Gráficos**

    # Grafico Técnicos

    # Filtrar técnicos que possuem mais de 1 conserto
    tecnico_filtrado = tecnico_count_df[tecnico_count_df['QUANTIDADE'] > 1]

    # Gráfico de barras para o número de consertos por funcionário
    plt.figure(figsize=(10, 6))
    plt.bar(tecnico_filtrado['TECNICO'], tecnico_filtrado['QUANTIDADE'], color='skyblue')
    plt.xlabel('Técnico')
    plt.ylabel('Número de Consertos')
    plt.title('Consertos por Funcionário')
    plt.xticks(rotation=90)  # Rotacionar os nomes dos técnicos para melhor visualização
    plt.tight_layout()
    plt.savefig('grafico_consertos_tecnicos.png')
    plt.close()

    # Análise adicional: Identificar o técnico mais produtivo
    if not tecnico_count_df.empty:
        top_tecnico = tecnico_count_df.loc[tecnico_count_df['QUANTIDADE'].idxmax()]
        print(f"\nTécnico mais produtivo: {top_tecnico['TECNICO']} com {top_tecnico['QUANTIDADE']} consertos.")

        # Comparar com a média da equipe
        media_equipe = tecnico_count_df['QUANTIDADE'].mean()
        print(f"Média de consertos por técnico (apenas com mais de 1 conserto): {media_equipe:.2f}.")

        # Identificar os técnicos acima da média
        acima_da_media = tecnico_count_df[tecnico_count_df['QUANTIDADE'] > media_equipe]
        print("\nTécnicos acima da média:")
        print(acima_da_media[['TECNICO', 'QUANTIDADE']])

    # Gráfico 1: Boxplot da distribuição do tempo de conserto
    if not df_unificado['TEMPO_CONSERTO'].dropna().empty:
        plt.figure(figsize=(10, 6))
        plt.boxplot(df_unificado['TEMPO_CONSERTO'].dropna(), vert=False, patch_artist=True, boxprops=dict(facecolor='skyblue'))
        plt.title('Distribuição do Tempo de Conserto (em dias)')
        plt.xlabel('Tempo de Conserto (dias)')
        plt.tight_layout()
        plt.savefig('boxplot_tempo_conserto.png')
        plt.close()

    # Agrupar por mês e calcular o tempo médio de conserto
    tempo_medio_por_mes = df_unificado.groupby('MES_ANO')['TEMPO_CONSERTO'].mean().reset_index()

    # Verificar se há dados para o gráfico 2
    if not tempo_medio_por_mes.empty:
        # Gráfico 2: Evolução do tempo médio de conserto ao longo do tempo
        plt.figure(figsize=(12, 6))
        plt.plot(tempo_medio_por_mes['MES_ANO'], tempo_medio_por_mes['TEMPO_CONSERTO'], marker='o', linestyle='-', color='skyblue')
        plt.title('Evolução do Tempo Médio de Conserto')
        plt.xlabel('Mês/Ano')
        plt.ylabel('Tempo Médio de Conserto (dias)')
        plt.xticks(rotation=90)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('linha_tempo_medio_conserto.png')
        plt.close()

    # **Gráfico Taxa de Sucesso para Conserto**

    # Padronizar novamente a coluna 'CONSERTADO' (caso não tenha sido padronizado anteriormente)
    df_unificado['CONSERTADO'] = df_unificado['CONSERTADO'].astype(str).str.strip().str.lower()
    df_unificado['CONSERTADO'] = df_unificado['CONSERTADO'].replace(valores_sim, 'sim')
    df_unificado = df_unificado[~df_unificado['CONSERTADO'].isin(valores_a_remover)]

    # Contagem atualizada de 'CONSERTADO'
    print("\nContagem atualizada de 'CONSERTADO':")
    print(df_unificado['CONSERTADO'].value_counts())

    # Gráfico de Pizza: Proporção de consertos bem-sucedidos versus não concluídos
    taxa_sucesso = df_unificado['CONSERTADO'].value_counts()

    plt.figure(figsize=(8, 8))
    taxa_sucesso.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightcoral'])
    plt.title('Taxa de Sucesso para Conserto')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('pizza_taxa_sucesso.png')
    plt.close()

    # **Gráfico de Aparelhos Recebidos ao Longo do Tempo**

    # Garantir que a coluna 'DATA' esteja no formato datetime
    df_unificado['DATA'] = pd.to_datetime(df_unificado['DATA'], format='%d/%m/%Y', errors='coerce')

    # Criar uma nova coluna com o período mensal (Mês/Ano no formato yyyy-mm)
    df_unificado['MES_ANO_DATA'] = df_unificado['DATA'].dt.to_period('M').astype(str)

    # Gráfico de Linhas: Número de aparelhos recebidos ao longo do tempo
    aparelhos_por_mes = df_unificado.groupby('MES_ANO_DATA').size().reset_index(name='QUANTIDADE')

    plt.figure(figsize=(12, 6))
    plt.plot(aparelhos_por_mes['MES_ANO_DATA'], aparelhos_por_mes['QUANTIDADE'], marker='o', linestyle='-', color='skyblue')
    plt.title('Número de Aparelhos Recebidos ao Longo do Tempo')
    plt.xlabel('Mês/Ano')
    plt.ylabel('Número de Aparelhos')
    plt.xticks(rotation=90)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('linha_aparelhos_recebidos.png')
    plt.close()

    # Gráfico de Barras: Comparar o número de aparelhos recebidos por categoria

    # Exemplo 1: Agrupar por marca
    if 'MARCA' in df_unificado.columns:
        aparelhos_por_marca = df_unificado['MARCA'].value_counts().reset_index()
        aparelhos_por_marca.columns = ['MARCA', 'QUANTIDADE']

        plt.figure(figsize=(12, 6))
        plt.bar(aparelhos_por_marca['MARCA'], aparelhos_por_marca['QUANTIDADE'], color='skyblue')
        plt.title('Número de Aparelhos Recebidos por Marca')
        plt.xlabel('Marca')
        plt.ylabel('Número de Aparelhos')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig('barra_aparelhos_por_marca.png')
        plt.close()

    # Exemplo 2: Agrupar por tipo de aparelho
    if 'APARELHO' in df_unificado.columns:
        aparelhos_por_tipo = df_unificado['APARELHO'].value_counts().reset_index()
        aparelhos_por_tipo.columns = ['APARELHO', 'QUANTIDADE']

        plt.figure(figsize=(12, 6))
        plt.bar(aparelhos_por_tipo['APARELHO'], aparelhos_por_tipo['QUANTIDADE'], color='lightcoral')
        plt.title('Número de Aparelhos Recebidos por Tipo de Aparelho')
        plt.xlabel('Tipo de Aparelho')
        plt.ylabel('Número de Aparelhos')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig('barra_aparelhos_por_tipo.png')
        plt.close()

    # Retornar os DataFrames processados para uso na aplicação
    return df_unificado, tecnico_count_df
