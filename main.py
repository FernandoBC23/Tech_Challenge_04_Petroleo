import streamlit as st
import pandas as pd 
# import streamlit_authenticator as stauthpip 


# pg = st.navigation(
#     {
#         "Home": [st.Page("homepage.py", title="HomePage")],
#         "Dashboard":[st.Page("dashboard.py", title="Dashboard"), 
#                      st.Page("indicadores.py", title="Indicadores")],
#         "Eventos":[st.Page("eventos.py", title="Eventos Históricos")]
#     }
# )

# pg.run()

import streamlit as st
from homepage import render_homepage
from dashboard import render_dashboard
from indicadores import render_indicadores
from eventos import render_eventos
from testes import render_testes

# Configuração da página - chamada única no início do script principal
# st.set_page_config(page_title="Análise do Petróleo", layout="wide")

# Dicionário de páginas e funções de renderização associadas
pages = {
    "HomePage": render_homepage,
    "Dashboard": render_dashboard,
    "Indicadores": render_indicadores,
    "Eventos Históricos": render_eventos,
    "Testes": render_testes
}

# Seleção de página com selectbox na barra lateral
page = st.sidebar.selectbox("Selecione a página", list(pages.keys()))

# Inserir uma barra de divisão no sidebar
st.sidebar.markdown("---")

# Executa a função associada à página selecionada
pages[page]()
