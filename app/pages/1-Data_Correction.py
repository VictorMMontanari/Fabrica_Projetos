import streamlit as st
import sys
from pathlib import Path
import streamlit as st
import os
import pandas as pd
# Adiciona o diretório src ao PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent.parent))

from src.data_correction import run_data_correction
from src.create_model import create_model

input_path = None
model_path = '/home/victor/workspace/Fabrica_Projetos/models/modelo_classificador_completo.joblib'

# run_data_correction(input_path, model_path)
st.set_page_config(layout="wide") 

st.header("Data Correction")

uploaded_files = []
df = None  # Variável global para guardar o último DataFrame
ds = None

with st.container():
    col1, col2= st.columns(2)
    with col1:
        uploaded_files = st.file_uploader(
            "Choose a CSV file", accept_multiple_files=True, type=["csv"]
        )
        
        input_dir = "/home/victor/workspace/Fabrica_Projetos/data/input/"
        os.makedirs(input_dir, exist_ok=True)  # Garante que o diretório exista

        for uploaded_file in uploaded_files:
            st.write("filename:", uploaded_file.name)

            save_path = os.path.join(input_dir, uploaded_file.name)

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"Arquivo salvo em: {save_path}")
            print(f"Arquivo salvo em: {save_path}")
            input_path = save_path
            # Lê o CSV para exibir mais tarde
            df = pd.read_csv(uploaded_file)
            print(df)
    with col2:
        st.markdown("""
        <style>
            .st-emotion-cache-u4v75y{
                margin-top: 12px;
                background-color: rgb(38, 39, 48);
                border-color: rgb(38, 39, 48);
                padding: 18px 16px 18px 16px;
            }
        </style>
    """, unsafe_allow_html=True)
        with st.container(border=True): 
            if st.button("Executar"):
                if input_path is not None:
                    st.write("Executando o modelo...")
                    success, output_file = run_data_correction(input_path, model_path)
                    if success:
                        st.success(f"Dados corrigidos salvos em: {output_file}")
                        ds = pd.read_csv(output_file)
                    else:
                        st.error("Erro durante a correção dos dados.")
                else:
                    st.error("Nenhum arquivo CSV carregado.")
with st.container():
    st.write("This is inside the container")
    col1, col2, col3 = st.columns([3, 1, 3])
    
    with col1:
        st.markdown("<h2 style='text-align: center'>Tabela de entrada</h2>", unsafe_allow_html=True)
        if df is not None:
            st.table(df)
        else:
            st.info("Nenhum CSV carregado.")

    with col2:
        st.markdown("<h2 style='text-align: center'>Carregando</h2>", unsafe_allow_html=True)

    with col3:
        st.markdown("<h2 style='text-align: center'>Tabela de saída</h2>", unsafe_allow_html=True)
        if ds is not None:
            st.table(ds)
        else:
            st.info("Nenhum CSV carregado.")