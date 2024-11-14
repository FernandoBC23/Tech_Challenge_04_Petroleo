import streamlit as st
import pandas as pd 
from data_loader import carregar_dados
import plotly.express as px

def render_testes():

    # Carregar os dados
    base_preco, base_demanda, base_producao = carregar_dados()

    # st.table(base_preco.head())

    # Converter a coluna "Date" para o formato de data    
    base_preco = base_preco.sort_values("Data")

    # Criar uma nova coluna "Month" que contém o ano e o mês
    base_preco["Ano"] = base_preco["Data"].apply(lambda x: str(x.year))

    # Criar uma seleção de meses na barra lateral do dashboard
    month = st.sidebar.selectbox("Selecione o Ano", base_preco["Ano"].unique())

    # Filtrar os dados com base no mês selecionado
    df_filtered = base_preco[base_preco["Ano"] == month]

    col1, col2 = st.columns(2) # Primeira linha com duas colunas
    col3, col4, col5 = st.columns(3) # Segunda linha com três colunas

    # ---------------------------------- Gráfico 01 -----------------------------------------

    # Criar o gráfico de faturamento por dia
    fig_date = px.bar(df_filtered, x="Data", y="Preço", color="Preço", title="Faturamento por dia")

    # Exibir o gráfico na primeira coluna
    col1.plotly_chart(fig_date, use_container_width=True)

    # ---------------------------------- Gráfico 02 -----------------------------------------
    
    # Calcular o faturamento total por cidade
    city_total = df_filtered.groupby("Data")[["Preço"]].sum().reset_index()

    # Criar o gráfico de barras para exibir o faturamento por cidade
    fig_city = px.bar(city_total, x="Data", y="Preço",
    title="Faturamento por cidade")

    # Exibir o gráfico na terceira coluna
    # col2.plotly_chart(fig_city, use_container_width=True)

    # ---------------------------------- Gráfico 03 -----------------------------------------
    
    # Extrair o ano e calcular a volatilidade anual (desvio padrão dos preços dentro de cada ano)
    base_preco['Ano'] = base_preco['Data'].dt.year
    volatilidade_anual = base_preco.groupby('Ano')['Preço'].std().reset_index()
    volatilidade_anual.columns = ['Ano', 'Volatilidade']  # Renomeia a coluna para "Volatilidade"

    # Calcular a média da volatilidade
    media_volatilidade = volatilidade_anual['Volatilidade'].mean()

    # Selecionar os 5 anos com maior volatilidade
    top_5_volatilidade = volatilidade_anual.nlargest(40, 'Volatilidade').sort_values('Volatilidade', ascending=False)

    # Criar gráfico de barras com personalização de cores e rótulos
    fig = px.bar(
        top_5_volatilidade,
        x='Ano',
        y='Volatilidade',
        orientation='v',  # Orientação vertical
        title="Anos onde a Volatilidade ficou acima da Média",
        labels={'Volatilidade': 'Volatilidade (Desvio Padrão)', 'Ano': 'Ano'},
        text='Volatilidade'  # Adiciona rótulo de valor
    )

    # Adicionar a linha horizontal com o valor médio da volatilidade
    fig.add_hline(y=media_volatilidade, line_dash="dash", line_color="red",
                  annotation_text=f"Média: {media_volatilidade:.2f}", 
                  annotation_position="top left")

    # Ajustar o layout do gráfico
    fig.update_traces(marker_color='#1665FD', marker_line_color='lightblue', marker_line_width=1.5, 
                      texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Volatilidade (Desvio Padrão)"
    ) 

    # Exibir o gráfico no Streamlit
    col2.plotly_chart(fig)


    # ---------------------------------- Gráfico 04 -----------------------------------------

    # Criar o gráfico de pizza para exibir o faturamento por tipo de pagamento
    fig_kind = px.pie(df_filtered, values="Preço", names="Ano",
                    title="Faturamento por tipo de pagamento")

    # Exibir o gráfico na quarta coluna
    col4.plotly_chart(fig_kind, use_container_width=True)