# main.py

from nicegui import ui
import quantix
import dashboard
import expenses
import books

def main():
    # Processar os dados uma única vez
    df_unificado, tecnico_count_df = quantix.process_data()

    # Configurar as páginas passando os DataFrames processados
    dashboard.setup_dashboard(df_unificado, tecnico_count_df)
    expenses.setup_expenses(df_unificado, tecnico_count_df)
    books.setup_books(df_unificado, tecnico_count_df)

    # Iniciar o servidor NiceGUI
    ui.run(title="Dashboard Análise de Consertos", port=8080)

if __name__ in {"__main__", "__mp_main__"}:
    main()
