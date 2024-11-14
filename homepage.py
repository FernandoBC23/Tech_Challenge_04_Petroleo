import streamlit as st
from PIL import Image

def render_homepage():

    # coluna_esquerda, coluna_direita = st.columns([1, 2])

    # Título da página inicial
    st.title("Análise do Petróleo Brent")

        # Descrição introdutória do projeto
    st.write("""
    ### Bem-vindo ao Dashboard de Análise do Petróleo Brent

    Este projeto foi desenvolvido com o objetivo de fornecer insights valiosos sobre a variação do preço do petróleo ao longo dos anos.
    Exploramos como eventos geopolíticos, crises econômicas e variações na demanda e produção impactam os preços, com o objetivo de auxiliar em tomadas de decisão informadas.
    """)

    # Adicionar uma imagem representativa
    try:
        image = Image.open("imagens/foto_capa_petroleo.webp")  # Substitua pelo caminho da sua imagem
        st.image(image, caption="Fonte: [Insira a fonte da imagem]", width=700)  # Altere o valor de width conforme desejado
    except FileNotFoundError:
        st.write("Imagem não encontrada. Verifique o caminho do arquivo.")
        

    # Seções de navegação
    st.markdown("### Navegação")
    st.write("""
    Explore as diferentes páginas para obter mais detalhes:
    - **Análise Histórica**: Visualize a evolução do preço do petróleo, com foco em eventos históricos e crises que influenciaram o mercado.
    - **Dashboard de Indicadores**: Encontre indicadores chave de preço, demanda e produção, com opções de filtro por período.
    - **Previsão de Preço (Machine Learning)**: Acesse as previsões de preço geradas por um modelo de Machine Learning.
    - **Deploy e Plano de Produção**: Saiba mais sobre o plano de deploy e produção do modelo e do dashboard.
    """)

    # Mensagem final para o usuário
    st.write("""
    Acompanhe a análise completa, entenda os eventos que moldaram o mercado de petróleo e visualize previsões para o futuro.
    Clique nas abas no menu à esquerda para explorar o dashboard!
    """)