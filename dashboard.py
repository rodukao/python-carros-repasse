import streamlit as st
import sqlite3
import pandas as pd
from modules.api_client import busca_moedas
from modules.database import salva_moedas, salva_veiculos
from modules.scraper import busca_itens

# Configurando página
st.set_page_config(
    page_title="Dashboard | Carros de Repasse",
    page_icon="img/car-icon.png",
    layout="wide"
)

# Título
st.title("Dashboard")

# botão atualização cotação de moedas
if st.button("Atualizar cotação"):
    cotacao_atual = busca_moedas()
    salva_moedas(cotacao_atual)

try:

    with st.spinner("Buscando dados..."):

        # traz cotação atual ou utiliza mais recente do banco
        try:
            cotacao_atual = busca_moedas()
            valor_bitcoin = cotacao_atual['bitcoin']
            valor_dolar = cotacao_atual['dolar']
        except Exception as e:
            print("Não foi possível pegar a cotação atual. Utilizando a mais recente.")
            with sqlite3.connect("data/monitor_repasse.db") as conexao:
                data_moedas = pd.read_sql_query(
                    "SELECT nome, valor_brl FROM moedas", conexao)
                valor_bitcoin = data_moedas[data_moedas['nome']
                                            == 'bitcoin']['valor_brl'].iloc[0]
                valor_dolar = data_moedas[data_moedas['nome']
                                          == 'dolar']['valor_brl'].iloc[0]

        # busca veículos
        with sqlite3.connect("data/monitor_repasse.db") as conexao:
            df = pd.read_sql_query(
                "SELECT titulo, preco_brl, quilometragem, ano, link FROM veiculos ORDER BY id DESC", conexao)

            # Filtros
            st.sidebar.header("Filtros")
            # preço
            preco_max = st.sidebar.slider(
                "Preço máximo (R$)", 0, 150000, 150000)
            df_filtrado = df[df['preco_brl'] <= preco_max].copy()

            # ano mínimo
            ano_min = (st.sidebar.text_input(
                "do ano", value="0", placeholder="ex: 2005"))
            if ano_min == "":
                ano_min = "0"

            # ano máximo
            ano_max = (st.sidebar.text_input(
                "até ano", value=df['ano'].max(), placeholder="ex: 2020"))
            if ano_max == "":
                ano_max = value = df['ano'].max()

            # filtra o dataframe
            df_filtrado = df_filtrado[df_filtrado['ano'].between(
                int(ano_min), int(ano_max))].copy()

            # Atualiza lista de veículos
            if st.sidebar.button("Atualizar veículos"):
                with st.status("Acessando OLX... isso pode levar alguns segundos", expanded=False) as status:
                    st.write("Buscando veículos...")
                    veiculos = busca_itens()
                    st.write("Salvando veículos no banco de dados")
                    salva_veiculos(veiculos)
                    status.update(label="Busca finalizada",
                                  state="complete", expanded=False)
                st.rerun()

            # Colunas
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    label="Total carros",
                    value=f"{len(df)}"
                )

            with col2:
                st.metric(
                    label="BTC",
                    value=f"{valor_bitcoin:,.2f}"
                )

            with col3:
                st.metric(
                    label="USD",
                    value=f"{valor_dolar:,.2f}"
                )

            # Calcula valor veículo com cotação das moedas
            df_filtrado['Preço (USD)'] = (
                df['preco_brl'] / valor_dolar).round(2)
            df_filtrado['Preço (BTC)'] = (
                df['preco_brl'] / valor_bitcoin).round(6)

            # Configura e mostra tabela
            st.dataframe(
                df_filtrado,
                column_config={
                    "link": st.column_config.LinkColumn(
                        "Link do anúncio",
                        help="Clique para abrir o anúncio",
                        display_text="Ver anúncio"
                    ),
                    "preco_brl": st.column_config.NumberColumn(
                        "Preço (BRL)",
                        format="R$ %.2f"
                    ),
                    "Preço (BTC)": st.column_config.NumberColumn(
                        "Preço (BTC)",
                        format="₿ %.6f"
                    ),
                    "Preço (USD)": st.column_config.NumberColumn(
                        "Preço (USD)",
                        format="$ %.2f"
                    )
                },
                hide_index=True
            )

            st.subheader("Distribuição de Preços por Ano")

            df_grafico = df_filtrado[df_filtrado['ano'] > 1900]
            st.scatter_chart(data=df_grafico, x="ano",
                             y="preco_brl", color="preco_brl")

except Exception as e:
    print("Erro ao conectar ao banco de dados: ", e)
