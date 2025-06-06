import streamlit as st
from PIL import Image

# Oculta o aviso de depreciação e remove espaço superior extra
st.set_page_config(layout="wide")

# Cria duas colunas com proporção 1:2
col1, col2 = st.columns([1, 2], gap="large")

# Coluna da imagem
with col1:
    st.markdown("<div style='display: flex; align-items: center; height: 100%;'>", unsafe_allow_html=True)
    image = Image.open("utils/assets/image.png")
    st.image(image, caption="DbClean em ação", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Coluna do texto
with col2:
    st.markdown("<div style='display: flex; flex-direction: column; justify-content: center; height: 100%;'>", unsafe_allow_html=True)
    st.markdown("## DbClean - Ferramenta de Correção de Dados com IA")

    st.markdown("""
    <div style="font-size: 1.1rem; line-height: 1.6;">
    <b>DbClean</b> é uma ferramenta desenvolvida para automatizar a limpeza e reorganização de dados empresariais,  
    utilizando técnicas de inteligência artificial.<br><br>
    Ideal para apoiar processos de migração de sistemas, reduzindo retrabalhos, erros e custos operacionais.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
