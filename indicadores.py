# import streamlit as st
# from data_loader import carregar_dados
# import pandas as pd
# import plotly.express as px

# # Carregar os dados
# base_preco, base_demanda, base_producao = carregar_dados()

# # Extrair o ano e o mês, criando colunas separadas para ambos
# base_preco['Ano'] = base_preco['Data'].dt.year
# base_preco['Mes'] = base_preco['Data'].dt.month

# # Obter os anos e meses únicos para os seletores
# anos_unicos = sorted(base_preco['Ano'].unique())

# # Seletor de período de anos
# anos_selecionados = st.select_slider(
#     "Selecione o Período de Anos",
#     options=anos_unicos,
#     value=(anos_unicos[0], anos_unicos[-1])
# )

# # Filtrar os dados para o intervalo de anos selecionado
# base_preco_filtrada = base_preco[(base_preco['Ano'] >= anos_selecionados[0]) & (base_preco['Ano'] <= anos_selecionados[1])]

# # Ordenar os dados em ordem crescente de data
# base_preco_filtrada = base_preco_filtrada.sort_values(by='Data')

# # Exibir gráfico de linha com base_preco nos dados filtrados
# if not base_preco_filtrada.empty:
#     grafico_linha = px.line(base_preco_filtrada, x="Data", y="Preço", 
#                             title="Variação do Preço do Petróleo Brent ao longo do tempo")
#     grafico_linha.update_layout(xaxis_title="Data", yaxis_title="Preço (USD)")
#     st.plotly_chart(grafico_linha)
# else:
#     st.write("Nenhum dado disponível para o intervalo selecionado.")

# # Função para criar cards
# def criar_card(icone, numero, texto, coluna_card):
#     container = coluna_card.container(border=True)
#     coluna_esquerda, coluna_direita = container.columns([1, 2.5])
#     coluna_esquerda.image(f"imagens/{icone}")
#     coluna_direita.write(numero)
#     coluna_direita.write(texto)

# # Colunas para os cards de indicadores básicos
# coluna_esquerda, coluna_meio, coluna_direita = st.columns([1, 1, 1])

# # Calcular e exibir indicadores básicos
# criar_card("noosfera.png", f'$ {base_preco_filtrada["Preço"].max()}', "Preço Máximo", coluna_esquerda)
# criar_card("noosfera.png", f'$ {base_preco_filtrada["Preço"].min()}', "Preço Mínimo", coluna_meio)
# criar_card("noosfera.png", f'$ {base_preco_filtrada["Preço"].mean().round(2)}', "Preço Médio", coluna_direita)

# # Cálculo da Variação Mensal
# base_preco_filtrada['Mes'] = base_preco_filtrada['Data'].dt.to_period('M')
# var_mensal = base_preco_filtrada.groupby('Mes')['Preço'].mean().pct_change().mean() * 100  # Percentual médio de variação mensal

# # Cálculo da Variação Anual
# base_preco_filtrada['Ano'] = base_preco_filtrada['Data'].dt.to_period('Y')
# var_anual = base_preco_filtrada.groupby('Ano')['Preço'].mean().pct_change().mean() * 100  # Percentual médio de variação anual

# # Cálculo do Retorno Acumulado
# preco_inicial = base_preco_filtrada['Preço'].iloc[0]
# preco_final = base_preco_filtrada['Preço'].iloc[-1]
# retorno_acumulado = ((preco_final / preco_inicial) - 1) * 100

# # Exibir novos indicadores
# coluna_esquerda_2, coluna_meio_2, coluna_direita_2 = st.columns([1, 1, 1])
# criar_card("noosfera.png", f'{var_mensal:.2f}%', "Variação Mensal Média", coluna_esquerda_2)
# criar_card("noosfera.png", f'{var_anual:.2f}%', "Variação Anual Média", coluna_meio_2)
# criar_card("noosfera.png", f'{retorno_acumulado:.2f}%', "Retorno Acumulado", coluna_direita_2)

# # Indicadores de Longo Prazo

# # Calcular CAGR (Taxa de Crescimento Anual Composta)
# n = anos_selecionados[1] - anos_selecionados[0] + 1
# if n > 1:
#     cagr = ((preco_final / preco_inicial) ** (1 / n) - 1) * 100
# else:
#     cagr = None  # Não faz sentido calcular CAGR para apenas um ano


# # Cálculo da Volatilidade Anual
# volatilidade_anual = base_preco_filtrada.groupby('Ano')['Preço'].std().mean()  # Média do desvio padrão anual


# # Exibir indicadores de longo prazo
# coluna_esquerda_3, coluna_meio_3, coluna_direita_3 = st.columns([1, 1, 1])
# criar_card("noosfera.png", f'{cagr:.2f}%', "CAGR", coluna_esquerda_3)
# criar_card("noosfera.png", f'{volatilidade_anual:.2f}', "Volatilidade Anual Média", coluna_meio_3)



import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data_loader import carregar_dados

def render_indicadores():
    # Carregar os dados
    base_preco, base_demanda, base_producao = carregar_dados()

    # Converter 'Data' para datetime e garantir ordenação
    base_preco['Data'] = pd.to_datetime(base_preco['Data'])
    base_preco = base_preco.sort_values(by='Data')  # Ordenar o DataFrame principal por data

    # Função para normalizar os dados entre 0 e 1
    def normalizar_serie(serie):
        return (serie - serie.min()) / (serie.max() - serie.min())

    # Sidebar para filtro de anos
    anos_unicos = sorted(base_preco['Data'].dt.year.unique())
    anos_selecionados = st.sidebar.select_slider(
        "Selecione o Período de Anos",
        options=anos_unicos,
        value=(anos_unicos[0], anos_unicos[-1])
    )

    # Filtrar os dados com base no intervalo de anos selecionado
    base_preco['Ano'] = base_preco['Data'].dt.year
    base_preco_filtrada = base_preco[(base_preco['Ano'] >= anos_selecionados[0]) & (base_preco['Ano'] <= anos_selecionados[1])]
    base_demanda_filtrada = base_demanda[(base_demanda['Ano'] >= anos_selecionados[0]) & (base_demanda['Ano'] <= anos_selecionados[1])].set_index('Ano').reindex(base_preco_filtrada['Ano']).reset_index()
    base_producao_filtrada = base_producao[(base_producao['Ano'] >= anos_selecionados[0]) & (base_producao['Ano'] <= anos_selecionados[1])].set_index('Ano').reindex(base_preco_filtrada['Ano']).reset_index()

    # Normalizar as séries de dados
    base_preco_filtrada['Preço_Normalizado'] = normalizar_serie(base_preco_filtrada['Preço'])
    base_demanda_filtrada['Demanda_Normalizada'] = normalizar_serie(base_demanda_filtrada['Total world'])
    base_producao_filtrada['Producao_Normalizada'] = normalizar_serie(base_producao_filtrada['Total World'])

    # ------------------- Seção de Indicadores Básicos -------------------
    st.title("Dashboard de Indicadores")
    st.subheader("Indicadores Básicos")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Preço Máximo", f"$ {base_preco_filtrada['Preço'].max():.2f}")
    col2.metric("Preço Mínimo", f"$ {base_preco_filtrada['Preço'].min():.2f}")
    col3.metric("Preço Médio", f"$ {base_preco_filtrada['Preço'].mean():.2f}")
    retorno_acumulado = ((base_preco_filtrada['Preço'].iloc[-1] / base_preco_filtrada['Preço'].iloc[0]) - 1) * 100
    col4.metric("Retorno Acumulado", f"{retorno_acumulado:.2f}%")

    # ------------------- Indicadores de Variação Mensal e Anual -------------------
    st.subheader("Indicadores de Variação")

    # Cálculo de Variação Mensal e Anual
    base_preco_filtrada['Mes'] = base_preco_filtrada['Data'].dt.to_period('M')
    var_mensal = base_preco_filtrada.groupby('Mes')['Preço'].mean().pct_change().mean() * 100
    base_preco_filtrada['Ano'] = base_preco_filtrada['Data'].dt.to_period('Y')
    var_anual = base_preco_filtrada.groupby('Ano')['Preço'].mean().pct_change().mean() * 100

    col1, col2 = st.columns(2)
    col1.metric("Variação Mensal Média", f"{var_mensal:.2f}%")
    col2.metric("Variação Anual Média", f"{var_anual:.2f}%")

    # ------------------- Gráfico Comparativo Normalizado -------------------
    st.subheader("Gráficos Comparativos Normalizados")
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=base_preco_filtrada['Data'], y=base_preco_filtrada['Preço_Normalizado'], mode='lines', name='Preço Normalizado'))
    fig.add_trace(go.Scatter(x=base_demanda_filtrada['Ano'], y=base_demanda_filtrada['Demanda_Normalizada'], mode='lines', name='Demanda Normalizada'))
    fig.add_trace(go.Scatter(x=base_producao_filtrada['Ano'], y=base_producao_filtrada['Producao_Normalizada'], mode='lines', name='Produção Normalizada'))

    fig.update_layout(
        title="Preço, Demanda e Produção de Petróleo (Normalizados)",
        xaxis_title="Ano",
        yaxis_title="Valor Normalizado",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )

    st.plotly_chart(fig)

    # ------------------- Seção de Volatilidade e Contexto Histórico -------------------
    st.subheader("Volatilidade e Contexto Histórico")

    # Para calcular a volatilidade, vamos definir 'Data' como o índice temporário
    base_preco_filtrada = base_preco_filtrada.set_index('Data')

    # Cálculo da volatilidade para períodos selecionados
    volatilidade_mensal = base_preco_filtrada['Preço'].resample('M').std().mean()
    volatilidade_anual = base_preco_filtrada['Preço'].resample('Y').std().mean()

    col1, col2 = st.columns(2)
    col1.metric("Volatilidade Mensal Média", f"{volatilidade_mensal:.2f}")
    col2.metric("Volatilidade Anual Média", f"{volatilidade_anual:.2f}")

    st.write("A volatilidade destaca a oscilação nos preços do petróleo, indicando períodos de instabilidade. Períodos com alta volatilidade tendem a coincidir com eventos geopolíticos críticos ou crises econômicas globais.")




