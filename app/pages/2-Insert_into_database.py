import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
import os
from pathlib import Path

DATA_DIR = "data/output"  # Pasta onde estão os CSVs
st.set_page_config(layout="wide") 

# Função para conectar ao MySQL
def create_mysql_connection(host, user, password, database):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database
        )
        st.success("Conexão estabelecida com sucesso!")
        return connection
    except Error as e:
        st.error(f"Erro ao conectar ao MySQL: {e}")
        return None


with st.container():
    col1, col2, col3= st.columns([3, 0.2, 3])
    with col1:
        st.title("Conexão com Banco de Dados MySQL")
        
        # Inicializa a conexão na sessão
        if 'mysql_conn' not in st.session_state:
            st.session_state.mysql_conn = None
        
        # Botão para abrir o modal de conexão
        if st.button("🔒 Conectar ao Banco de Dados"):
            st.session_state.show_connection_modal = True
        
        # Modal de conexão (implementado com expander)
        if st.session_state.get('show_connection_modal', False):
            with st.expander("🔒 Configurações de Conexão MySQL", expanded=True):
                host = st.text_input("Host", "localhost")
                user = st.text_input("Usuário", "root")
                password = st.text_input("Senha", type="password")
                database = st.text_input("Banco de Dados")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Conectar"):
                        conn = create_mysql_connection(host, user, password, database)
                        if conn:
                            st.session_state.mysql_conn = conn
                            st.session_state.show_connection_modal = False
                
                with col2:
                    if st.button("Cancelar"):
                        st.session_state.show_connection_modal = False
        
        # Se conectado, mostra informações e opções
        if st.session_state.mysql_conn:
            st.success("✅ Conectado ao banco de dados")
            
            # Exemplo: mostrar tabelas
            if st.button("Mostrar tabelas"):
                try:
                    cursor = st.session_state.mysql_conn.cursor()
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    st.write("Tabelas no banco de dados:")
                    for table in tables:
                        st.write(table[0])
                except Error as e:
                    st.error(f"Erro ao listar tabelas: {e}")
            
            # Botão para desconectar
            if st.button("Desconectar"):
                st.session_state.mysql_conn.close()
                st.session_state.mysql_conn = None
                st.success("Desconectado com sucesso!")
                
    with col3:
        st.title("Selecione o CSV corrigido")
        
        if st.session_state.mysql_conn:
            # Listar arquivos CSV da pasta data/output
            try:
                csv_files = [f for f in os.listdir("data/output") if f.endswith('.csv')]
                
                if not csv_files:
                    st.warning("Nenhum arquivo CSV encontrado na pasta data/output")
                else:
                    selected_file = st.selectbox("Arquivos CSV disponíveis:", csv_files)
                    
                    # Visualização do CSV selecionado
                    if st.checkbox("Visualizar dados do CSV"):
                        try:
                            df = pd.read_csv(f"data/output/{selected_file}")
                            st.dataframe(df)
                        except Exception as e:
                            st.error(f"Erro ao ler o arquivo CSV: {str(e)}")
                    
                    # Listar tabelas do banco para seleção
                    try:
                        cursor = st.session_state.mysql_conn.cursor()
                        cursor.execute("SHOW TABLES")  # Corrigido aqui
                        tables = [table[0] for table in cursor.fetchall()]
                        
                        if not tables:
                            st.warning("Nenhuma tabela encontrada no banco de dados")
                        else:
                            selected_table = st.selectbox("Selecione a tabela de destino:", tables)
                            
                            # Opção para importar
                            if st.button("Importar para o MySQL"):
                                try:
                                    df = pd.read_csv(f"data/output/{selected_file}")
                                    
                                    # Obter colunas da tabela MySQL
                                    cursor.execute(f"DESCRIBE {selected_table}")
                                    table_columns = [column[0] for column in cursor.fetchall()]
                                    
                                    # Verificar compatibilidade de colunas
                                    if not all(col in table_columns for col in df.columns):
                                        missing = set(df.columns) - set(table_columns)
                                        st.error(f"Colunas faltando na tabela: {', '.join(missing)}")
                                    else:
                                        # Preparar query de inserção
                                        placeholders = ', '.join(['%s'] * len(df.columns))
                                        columns = ', '.join(df.columns)
                                        query = f"INSERT INTO {selected_table} ({columns}) VALUES ({placeholders})"
                                        
                                        # Converter DataFrame para lista de tuplas
                                        data = [tuple(row) for row in df.values]
                                        
                                        # Executar inserções em lote
                                        cursor.executemany(query, data)
                                        st.session_state.mysql_conn.commit()
                                        
                                        st.success(f"{len(data)} registros importados com sucesso para {selected_table}!")
                                        
                                except Error as e:
                                    st.session_state.mysql_conn.rollback()
                                    st.error(f"Erro no MySQL: {str(e)}")
                                except Exception as e:
                                    st.error(f"Erro geral: {str(e)}")
                                finally:
                                    cursor.close()
                    
                    except Error as e:
                        st.error(f"Erro ao listar tabelas: {str(e)}")
                    finally:
                        if 'cursor' in locals():
                            cursor.close()
            
            except FileNotFoundError:
                st.error("Pasta data/output não encontrada")
            except Exception as e:
                st.error(f"Erro inesperado: {str(e)}")
        else:
            st.warning("Conecte-se ao banco de dados primeiro")