# **Quantix**

## **Descrição**
Este projeto é um painel interativo desenvolvido em **NiceGUI** e **Python** que analisa dados de consertos e despesas operacionais. Ele oferece gráficos, tabelas e insights para ajudar empresas a tomarem decisões estratégicas com base em grandes volumes de dados.

---

## **Funcionalidades**

### **Painel Centralizado**
- Resumo visual de métricas de desempenho:
  - Tempo médio de conserto.
  - Taxa de sucesso.
  - Número de aparelhos recebidos.
- Navegação intuitiva com páginas dedicadas.

### **Análise de Consertos**
- Identificação dos técnicos mais produtivos.
- Gráficos interativos, como:
  - Distribuição do tempo de conserto.
  - Taxa de sucesso de consertos.

### **Análise de Despesas**
- Detalhamento de despesas por:
  - Categoria.
  - Formas de pagamento.
  - Situação de pagamento (Pago x Não Pago).
- Evolução mensal de despesas para as 10 categorias principais.

### **Exemplos Fictícios**
- Uma página adicional demonstra funcionalidades de gráficos de barras, linhas e agrupados, para fins de aprendizado e personalização.

---

## **Tecnologias Utilizadas**
- **Python 3.11**: Linguagem base para desenvolvimento.
- **[NiceGUI](https://nicegui.io/)**: Framework para criar interfaces web interativas.
- **[Pandas](https://pandas.pydata.org/)**: Manipulação e análise de dados.
- **[Matplotlib](https://matplotlib.org/)**: Criação de gráficos para análise visual.
- **[Seaborn](https://seaborn.pydata.org/)**: Estilização adicional dos gráficos.

---

## **Requisitos**
1. **Python 3.10+**
2. Instale as dependências necessárias:
   ```bash
   pip install nicegui pandas matplotlib seaborn

---

## **Como Executar**

### **1. Clone o Repositório**
```bash
git clone <url-do-repositorio>
cd <nome-do-projeto>
```

### **2. Certifique-se de que os Dados Estão na Pasta Correta**
Coloque os arquivos de despesas e consertos na pasta `data/`.

### **3. Inicie o Servidor**
Execute o arquivo `main.py`:
```bash
python main.py
```

---

## **Seções do Painel**

### **1. Dashboard Principal**
- **Local:** `/`
- **Gráficos Disponíveis:**
  - Distribuição do tempo de conserto (Boxplot).
  - Evolução do tempo médio de conserto.
  - Taxa de sucesso dos consertos.
  - Número de aparelhos recebidos ao longo do tempo.

### **2. Análise de Despesas**
- **Local:** `/expenses`
- **Gráficos Disponíveis:**
  - Despesas por categoria (barras).
  - Proporção das formas de pagamento (pizza).
  - Evolução mensal de despesas (Top 10 categorias).
  - Situação de pagamento (barras).

### **3. Página de Livros (Exemplo Fictício)**
- **Local:** `/books`
- **Gráficos de Demonstração:**
  - Barras.
  - Linhas.
  - Barras agrupadas.

---

## **Como Personalizar**

### **Adicionar Novos Dados**
- Coloque arquivos CSV na pasta `data/`.
- Ajuste o processamento em `quantix.py` ou `expenses.py`.

### **Alterar Gráficos ou Métricas**
- Edite as funções de geração de gráficos nos arquivos:
  - `quantix.py`: Para dados de consertos.
  - `expenses.py`: Para dados de despesas.

### **Adicionar Novas Páginas**
- Siga o padrão de criação de páginas do NiceGUI:
  - Use exemplos nos arquivos `dashboard.py` e `books.py`.
