import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data_loader import carregar_dados
import plotly.express as px

def render_dashboard():   

    # Carregar os dados
    base_preco, base_demanda, base_producao = carregar_dados()

     # Adicionar opções de visualização no sidebar
    st.sidebar.write("### Selecione a Visualização")
    opcao_dados = st.sidebar.radio("Dados:", ["Preço", "Demanda e Produção", "Todos", "Comparação"])

    st.sidebar.markdown("_________________")

    # Extrair o ano e o mês, criando colunas separadas para ambos
    base_preco['Ano'] = base_preco['Data'].dt.year
    base_preco['Mes'] = base_preco['Data'].dt.month

    # Obter os anos e meses únicos para os seletores
    anos_unicos = sorted(base_preco['Ano'].unique())

    # Seletor de período de anos
    anos_selecionados = st.sidebar.select_slider(
        "Selecione o Período de Anos",
        options=anos_unicos,
        value=(anos_unicos[0], anos_unicos[-1])
    )

    # Filtrar os dados para o intervalo de anos selecionado
    base_preco_filtrada = base_preco[(base_preco['Ano'] >= anos_selecionados[0]) & (base_preco['Ano'] <= anos_selecionados[1])]

    # Ordenar os dados em ordem crescente de data
    base_preco_filtrada = base_preco_filtrada.sort_values(by='Data')

# -------------------------------------------------------------------------------------------
    # Função para criar cards com tamanho de fonte personalizado
    def criar_card(icone, numero, texto, coluna_card):
        container = coluna_card.container()
        container = coluna_card.container(border=True)
        coluna_esquerda, coluna_direita = container.columns([1, 4])

        # Adiciona o ícone à esquerda
        coluna_esquerda.image(f"imagens/{icone}")
        
        # Usa CSS para personalizar o tamanho da fonte
        coluna_direita.markdown(
            f"""
            <div style="font-size:32px; font-weight:bold;">{numero}</div>           
            """,
            unsafe_allow_html=True
        )

        # Usa CSS para personalizar o tamanho da fonte e alinhamento
        container.markdown(
            f"""            
            <div style="font-size:16px; color:grey; text-align: center;">{texto}</div>
            """,
            unsafe_allow_html=True
        )
# ------------------------------------------------------------------------------------------
    # Condições de visualização
    if opcao_dados == "Preço":   

        # Colunas para os cards de indicadores básicos
        # col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
                
        # Calcular e exibir indicadores básicos
        criar_card("aumentar_1.png", f'${base_preco_filtrada["Preço"].max()}', "Preço Máximo", col1)
        criar_card("diminuir_1.png", f'${base_preco_filtrada["Preço"].min()}', "Preço Mínimo", col2)
        criar_card("preco_medio.png", f'${base_preco_filtrada["Preço"].mean().round(2)}', "Preço Médio", col3)
        retorno_acumulado = ((base_preco_filtrada['Preço'].iloc[-1] / base_preco_filtrada['Preço'].iloc[0]) - 1) * 100
        criar_card("acumulado.png", f'{retorno_acumulado:.2f}%', "Retorno Acumulado", col4)

        # Cálculo de Variação Mensal e Anual
        base_preco_filtrada['Mes'] = base_preco_filtrada['Data'].dt.to_period('M')
        var_mensal = base_preco_filtrada.groupby('Mes')['Preço'].mean().pct_change().mean() * 100
        base_preco_filtrada['Ano'] = base_preco_filtrada['Data'].dt.to_period('Y')
        var_anual = base_preco_filtrada.groupby('Ano')['Preço'].mean().pct_change().mean() * 100

        # -----------------------------------------------------------------------------------------------

        # Exibir gráfico de linha com base_preco nos dados filtrados
        if not base_preco_filtrada.empty:
            grafico_linha = px.line(base_preco_filtrada, x="Data", y="Preço", 
                                    title="Variação do Preço do Petróleo Brent ao longo do tempo")
            grafico_linha.update_layout(xaxis_title="Data", yaxis_title="Preço (USD)")
            st.plotly_chart(grafico_linha)
        else:
            st.write("Nenhum dado disponível para o intervalo selecionado.")

        # -----------------------------------------------------------------------------------------------

        # Colunas para os cards de indicadores básicos
        # col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        col1, col2 = st.columns([1, 4])

        # Para calcular a volatilidade, vamos definir 'Data' como o índice temporário
        base_preco_filtrada = base_preco_filtrada.set_index('Data')

        # Cálculo da volatilidade para períodos selecionados
        volatilidade_mensal = base_preco_filtrada['Preço'].resample('M').std().mean()
        volatilidade_anual = base_preco_filtrada['Preço'].resample('Y').std().mean()

        base_preco_filtrada = base_preco_filtrada.reset_index()  # Restaurar a coluna "Data"

        # criar_card("noosfera.png", f'{var_mensal:.2f}%', "Variação Mensal Média", col1)      
        # criar_card("noosfera.png", f'{var_anual:.2f}%', "Variação Anual Média", col2)
        criar_card("aumentar.png", f'{volatilidade_mensal:.2f}%', "", col1)
        
        # Exibir uma lista formatada sobre alta e baixa volatilidade
        col2.markdown("""
            <ul style="font-size:16px; color:grey; line-height:1.6;">
                <li><b>Alta volatilidade:</b> Sinaliza um mercado mais arriscado e incerto, onde os preços estão sujeitos a mudanças bruscas. Isso pode oferecer oportunidades de ganhos,
                    mas também aumenta o potencial de perdas.</li>
                <li><b>Baixa volatilidade:</b> Indica um mercado mais estável, com variações de preço mais suaves e previsíveis. Embora seja menos arriscado, também tende a oferecer retornos menores.</li>
            </ul>
        """, unsafe_allow_html=True)


        criar_card("diminuir.png", f'{volatilidade_anual:.2f}%', "", col1)

        # Adicionar a descrição da volatilidade
        col2.markdown("""
            <p style="font-size:16px; color:grey; line-height:1.6;">
                A volatilidade destaca a oscilação nos preços do petróleo, indicando períodos de instabilidade. Períodos com alta volatilidade tendem a coincidir
                com eventos geopolíticos críticos ou crises econômicas globais.
            </p>
        """, unsafe_allow_html=True)                




    elif opcao_dados == "Demanda e Produção":
        # Indicadores de Demanda e Produção
        st.write("## Indicadores de Demanda e Produção")


    elif opcao_dados == "Todos":
        # Exibir todos os indicadores e gráficos divididos em colunas
        st.write("## Indicadores de Preço, Demanda e Produção")


    elif opcao_dados == "Comparação":
        # Opções de comparação
        st.sidebar.write("### Selecione Comparação")


