import streamlit as st
import pandas as pd 

@st.cache_data
def carregar_dados():
    # Carregar o arquivo de preço do petróleo
    tabela_preco = pd.read_excel("Dados/preco_petroleo_brent.xlsx")
    tabela_preco = tabela_preco.rename(columns={"Preço - petróleo bruto - Brent (FOB)": "Preço"})
    
    # Carregar o arquivo de demanda de petróleo
    tabela_demanda = pd.read_excel("Dados/Demanda_Mundial_Petroleo.xlsx")
    # tabela_demanda = tabela_demanda.rename(columns={"Demanda - petróleo bruto": "Demanda"})  # Ajuste o nome da coluna conforme necessário
    
    # Carregar o arquivo de produção de petróleo
    tabela_producao = pd.read_excel("Dados/Producao_Mundial_Petroleo.xlsx")
    # tabela_producao = tabela_producao.rename(columns={"Produção - petróleo bruto": "Produção"})  # Ajuste o nome da coluna conforme necessário
    
    return tabela_preco, tabela_demanda, tabela_producao

# Carregar os dados
base_preco, base_demanda, base_producao = carregar_dados()