import streamlit as st
import sys
from pathlib import Path
import streamlit as st
import os
import pandas as pd
import time


# Adiciona o diretório src ao PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent.parent))

from src.data_correction import run_data_correction
from src.create_model import create_model

input_path = None
model_path = 'models/modelo_classificador_completo.joblib'

# run_data_correction(input_path, model_path)
st.set_page_config(layout="wide") 

st.header("Data Correction")

uploaded_files = []
df = None  # Variável global para guardar o último DataFrame
ds = None

with st.container():

    if "executar_modelo" not in st.session_state:
        st.session_state.executar_modelo = False

    if "executado" not in st.session_state:
        st.session_state.executado = False

    col1, col2= st.columns(2)
    with col1:
        uploaded_files = st.file_uploader(
            "Choose a CSV file", accept_multiple_files=True, type=["csv"]
        )
        
        input_dir = "data/input/"
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
        with st.container(border=True): 
            if st.button("Executar"):
                st.session_state.executar_modelo = True
                if input_path is not None:
                    st.write("Executando o modelo...")
                    success, output_file = run_data_correction(input_path, model_path)
                    if success:
                        st.success(f"Dados corrigidos salvos em: {output_file}")
                        ds = pd.read_csv(output_file)
                        st.session_state.executado = False
                    else:
                        st.error("Erro durante a correção dos dados.")
                else:
                    st.error("Nenhum arquivo CSV carregado.")
with st.container():
    st.write("This is inside the container")
    col1, col2, col3 = st.columns([3, 1, 3])
    
    # Definir altura máxima para as tabelas (em pixels)
    table_height = "400px"
    table_width = "900px"
    
    with col1:
        st.markdown("<h2 style='text-align: center'>Tabela de entrada</h2>", unsafe_allow_html=True)
        if df is not None:
            st.markdown(
                f"""
                <div style='height: {table_height}; max-width: {table_width}; overflow-y: auto; border: 1px solid #ccc; border-radius: 5px;'>
                    {df.to_html()}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("Nenhum CSV carregado.")

    with col2:
        #st.markdown("<h2 style='text-align: center'>Carregando</h2>", unsafe_allow_html=True)
        if st.session_state.executar_modelo and not st.session_state.executado:
            with st.spinner("Executando o modelo..."):
                time.sleep(5)  # Aqui entraria sua função real
                st.session_state.executado = True
                st.session_state.executar_modelo = False  # Reseta a flag após execução
            st.success("Processamento finalizado com sucesso!")

        elif st.session_state.executado:
            st.info("O modelo já foi executado. Você pode rodar novamente se quiser.")

    with col3:
        st.markdown("<h2 style='text-align: center'>Tabela de saída</h2>", unsafe_allow_html=True)
        if ds is not None:
            st.markdown(
                f"""
                <div style='height: {table_height}; max-width: {table_width};overflow-y: auto; border: 1px solid #ccc; border-radius: 5px;'>
                    {ds.to_html()}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("Nenhum CSV carregado.")

st.markdown("""
        <style>
            .st-emotion-cache-u4v75y{
                    margin-top: 29px;
                    background-color: rgb(38, 39, 48);
                    border-color: rgb(38, 39, 48);
                    padding: 18px 16px 18px 16px;
                }
            .st-emotion-cache-1ikixyd {
                   display: flex;
                   align-items: center;
                   justify-content: center;
            }         
        </style>
    """, unsafe_allow_html=True)