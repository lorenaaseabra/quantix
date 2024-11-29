# quantix.py

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import re
import os

# Configurações do Matplotlib
matplotlib.rcParams['font.family'] = 'Arial'

def process_data():
    # Definir o diretório de saída para os gráficos
    BASE_DIR = os.getcwd()
    OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'outputs')
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # Criar a pasta, se não existir

    # Caminho para os arquivos CSV
    caminho_dados = os.path.join(BASE_DIR, 'data')

    # Leitura dos arquivos CSV
    df2018 = pd.read_csv(os.path.join(caminho_dados, 'Dados_Tratados_Normalizados_2018 - Dados_Normalizados_Eceel_Tec.csv'))
    df2020 = pd.read_csv(os.path.join(caminho_dados, 'Dados_Tratados_Normalizados_2020 - Dados_Normalizados_Eceel_Tec_2020.csv'))
    df2021 = pd.read_csv(os.path.join(caminho_dados, 'Dados_Normalizados_ECEEL_TEC_2021 - Dados_Normalizados_ECEEL_TEC_2021.csv'))
    df2022 = pd.read_csv(os.path.join(caminho_dados, 'Dados_Tratados_Normalizados_2022 - Dados_Tratados_Normalizados_2022.csv'))
    df2023 = pd.read_csv(os.path.join(caminho_dados, 'Dados_Tratados_ECEEL_TEC_2023 - Dados_Tratados_ECEEL_TEC_2023.csv'))
    df2024 = pd.read_csv(os.path.join(caminho_dados, 'Dados_Tratados_e_Normalizados_ECEEL_TEC_2024 - Dados_Tratados_e_Normalizados_ECEEL_TEC.csv'))

    # **Tratamento das planilhas**

    ## Unificação das tabelas

    # Remover a coluna 'ORDEM' de 2022, caso ela exista
    if 'ORDEM' in df2022.columns:
        df2022 = df2022.drop(columns=['ORDEM'])

    # Renomear as colunas para garantir consistência nos nomes
    rename_columns = {
        'CONSERTADO?': 'CONSERTADO',
        'PEÇA RECEBIDA': 'PECA_RECEBIDA',
        'SAÍDA': 'SAIDA',
        'TIPO_DE_AT': 'TIPO DE AT.'
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
        .str.replace(r'\s+e\s+', '/', regex=True)
        .str.replace(r'\s+E\s+', '/', regex=True)
        .str.replace(r'\s*,\s*', '/', regex=True)
        .str.replace(r'\s*-\s*', '/', regex=True)
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
    tecnico_count_df.to_csv(os.path.join(caminho_dados, 'tecnico_count.csv'), index=False)

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

    df_unificado.to_csv(os.path.join(caminho_dados, 'Dados_Unificados.csv'), index=False)

    # **Gráficos para Dashboard**

    # Gráfico 1: Boxplot da distribuição do tempo de conserto
    if not df_unificado['TEMPO_CONSERTO'].dropna().empty:
        plt.figure(figsize=(10, 6))
        plt.boxplot(df_unificado['TEMPO_CONSERTO'].dropna(), vert=False, patch_artist=True, boxprops=dict(facecolor='skyblue'))
        plt.title('Distribuição do Tempo de Conserto (em dias)')
        plt.xlabel('Tempo de Conserto (dias)')
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'boxplot_tempo_conserto.png'))
        plt.close()

    # Gráfico 2: Evolução do tempo médio de conserto ao longo do tempo
    tempo_medio_por_mes = df_unificado.groupby('MES_ANO')['TEMPO_CONSERTO'].mean().reset_index()

    if not tempo_medio_por_mes.empty:
        plt.figure(figsize=(12, 6))
        plt.plot(tempo_medio_por_mes['MES_ANO'], tempo_medio_por_mes['TEMPO_CONSERTO'], marker='o', linestyle='-', color='skyblue')
        plt.title('Evolução do Tempo Médio de Conserto')
        plt.xlabel('Mês/Ano')
        plt.ylabel('Tempo Médio de Conserto (dias)')
        plt.xticks(rotation=90)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'linha_tempo_medio_conserto.png'))
        plt.close()

    # Gráfico 3: Taxa de Sucesso para Conserto
    # Padronizar novamente a coluna 'CONSERTADO' (caso não tenha sido padronizado anteriormente)
    df_unificado['CONSERTADO'] = df_unificado['CONSERTADO'].astype(str).str.strip().str.lower()
    df_unificado['CONSERTADO'] = df_unificado['CONSERTADO'].replace(valores_sim, 'sim')
    df_unificado = df_unificado[~df_unificado['CONSERTADO'].isin(valores_a_remover)]

    # Contagem atualizada de 'CONSERTADO'
    taxa_sucesso = df_unificado['CONSERTADO'].value_counts()

    plt.figure(figsize=(8, 8))
    taxa_sucesso.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightcoral'])
    plt.title('Taxa de Sucesso para Conserto')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'pizza_taxa_sucesso.png'))
    plt.close()

    # Gráfico 4: Número de Aparelhos Recebidos ao Longo do Tempo
    # Garantir que a coluna 'DATA' esteja no formato datetime
    if 'DATA' in df_unificado.columns:
        df_unificado['DATA'] = pd.to_datetime(df_unificado['DATA'], format='%d/%m/%Y', errors='coerce')
        df_unificado['MES_ANO_DATA'] = df_unificado['DATA'].dt.to_period('M').astype(str)

        aparelhos_por_mes = df_unificado.groupby('MES_ANO_DATA').size().reset_index(name='QUANTIDADE')

        plt.figure(figsize=(12, 6))
        plt.plot(aparelhos_por_mes['MES_ANO_DATA'], aparelhos_por_mes['QUANTIDADE'], marker='o', linestyle='-', color='skyblue')
        plt.title('Número de Aparelhos Recebidos ao Longo do Tempo')
        plt.xlabel('Mês/Ano')
        plt.ylabel('Número de Aparelhos')
        plt.xticks(rotation=90)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'linha_aparelhos_recebidos.png'))
        plt.close()

    # Gráfico 5: Número de Aparelhos Recebidos por Marca
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
        plt.savefig(os.path.join(OUTPUT_DIR, 'barra_aparelhos_por_marca.png'))
        plt.close()

    # Gráfico 6: Número de Aparelhos Recebidos por Tipo de Aparelho
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
        plt.savefig(os.path.join(OUTPUT_DIR, 'barra_aparelhos_por_tipo.png'))
        plt.close()

    # **Gráficos para Dashboard**

    # Gráfico 7: Gráfico de Barras para o número de consertos por técnico
    tecnico_filtrado = tecnico_count_df[tecnico_count_df['QUANTIDADE'] > 1]

    plt.figure(figsize=(10, 6))
    plt.bar(tecnico_filtrado['TECNICO'], tecnico_filtrado['QUANTIDADE'], color='skyblue')
    plt.xlabel('Técnico')
    plt.ylabel('Número de Consertos')
    plt.title('Consertos por Funcionário')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'grafico_consertos_tecnicos.png'))
    plt.close()

    # **Processamento de Dados de Despesas**

    # Leitura dos arquivos de despesas
    despesas_path = os.path.join(caminho_dados, 'Despesas 2024-2018.csv')
    tratamento_path = os.path.join(caminho_dados, 'Tratamento dos dados - 2021.csv')

    # Verificar se os arquivos existem
    if os.path.exists(despesas_path):
        dados_despesas = pd.read_csv(despesas_path)

        # Mapeamento de meses para números
        meses_dict = {
            'Janeiro': '01', 'Fevereiro': '02', 'Março': '03', 'Abril': '04',
            'Maio': '05', 'Junho': '06', 'Julho': '07', 'Agosto': '08',
            'Setembro': '09', 'Outubro': '10', 'Novembro': '11', 'Dezembro': '12'
        }

        dados_despesas['Mês_Num'] = dados_despesas['Mês'].map(meses_dict)
        dados_despesas['Data'] = pd.to_datetime(
            dados_despesas['Data de Preenchimento'].astype(str) + '/' + dados_despesas['Mês_Num'] + '/2021',
            format='%d/%m/%Y',
            errors='coerce'
        )

        dados_despesas['Valor (R$)'] = (
            dados_despesas['Valor (R$)']
            .str.replace('$', '', regex=False)
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
            .astype(float)
        )

        # Gráfico 1: Despesas Mensais por Categoria (Top 10)
        valor_total_por_categoria = (
            dados_despesas.groupby('Categoria')['Valor (R$)']
            .sum()
            .sort_values(ascending=False)
        )

        top_10_categorias = valor_total_por_categoria.head(10).index
        dados_filtrados_despesas = dados_despesas[
            dados_despesas['Categoria'].isin(top_10_categorias)
        ]

        fig_top_categorias = plt.figure(figsize=(12, 6))
        for categoria in top_10_categorias:
            gastos_categoria = dados_filtrados_despesas[dados_filtrados_despesas['Categoria'] == categoria]
            gastos_categoria_mensal = (
                gastos_categoria.groupby(dados_filtrados_despesas['Data'].dt.month)['Valor (R$)']
                .sum()
            )
            plt.plot(
                gastos_categoria_mensal.index,
                gastos_categoria_mensal.values,
                marker='o',
                label=categoria,
            )
        plt.title('Despesas Mensais por Categoria (Top 10)')
        plt.xlabel('Mês')
        plt.ylabel('Total de Despesas (R$)')
        plt.legend(
            loc='lower center',
            bbox_to_anchor=(0.2, -0.35, 0.5, 0.2),
            ncol=4,
            fontsize=10,
        )
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'despesas_mensais_top10.png'))
        plt.close()
    else:
        print(f"Arquivo {despesas_path} não encontrado.")

    if os.path.exists(tratamento_path):
        dados_tratamento = pd.read_csv(tratamento_path)

        dados_tratamento['Valor'] = dados_tratamento['Valor'].replace(
            '[R$\s]', '', regex=True).str.replace(',', '').astype(float)
        dados_tratamento['Forma de Pagamento'] = dados_tratamento['Forma de Pagamento'].fillna('Forma de Pagamento não definido')
        dados_tratamento['Parcela'] = dados_tratamento['Parcela'].fillna('1/1')

        dados_tratamento['Mês_Num'] = dados_tratamento['Mês'].map(meses_dict)
        dados_tratamento['Data'] = pd.to_datetime(
            dados_tratamento['Dia'].astype(str) + '/' + dados_tratamento['Mês_Num'] + '/2021',
            format='%d/%m/%Y',
            errors='coerce'
        )

        # Gráfico 2: Despesas por Categoria (Bar)
        custo_categoria = dados_tratamento.groupby('Categoria')['Valor'].sum()

        fig_despesa_categoria = plt.figure(figsize=(10, 5))
        custo_categoria.plot(kind='bar', color='skyblue')
        plt.title('Despesas por Categoria')
        plt.xlabel('Categoria')
        plt.ylabel('Custo Total (R$)')
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'despesas_por_categoria.png'))
        plt.close()

        # Gráfico 3: Distribuição das Formas de Pagamento (Pie)
        formas_pagamento = dados_tratamento['Forma de Pagamento'].value_counts()
        fig_formas_pagamento = plt.figure(figsize=(10, 5))
        formas_pagamento.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Distribuição das Formas de Pagamento')
        plt.ylabel('')  # Remove o label padrão do eixo y
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'distribuicao_formas_pagamento.png'))
        plt.close()

        # Gráfico 4: Situação de Pagamento (Bar)
        dados_tratamento['Situação'] = dados_tratamento['Situação'].fillna('Não Pago')
        situacao_proporcao = dados_tratamento['Situação'].value_counts()

        fig_situacao_pagamento = plt.figure(figsize=(8, 5))
        situacao_proporcao.plot(kind='bar', color='coral')
        plt.title('Proporção de Situação de Pagamento')
        plt.xlabel('Situação')
        plt.ylabel('Quantidade de Transações')
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'proporcao_situacao_pagamento.png'))
        plt.close()
    else:
        print(f"Arquivo {tratamento_path} não encontrado.")

    # Retornar os DataFrames processados para uso na aplicação
    return df_unificado, tecnico_count_df
