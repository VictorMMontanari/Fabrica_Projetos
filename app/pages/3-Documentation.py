import streamlit as st

# Configuração da página
st.set_page_config(page_title="Documentation", layout="centered")

# Cabeçalho
st.title("📚 Documentação do Projeto DbClean")

# Descrição inicial
st.markdown("""
Este projeto é uma ferramenta de **correção e classificação de dados** que utiliza modelos de _machine learning_ para limpar, reorganizar e classificar dados empresariais durante processos de migração.

A seguir estão os principais módulos que compõem o sistema:
""")

# Componentes principais com markdown formatado
st.markdown("""
### 🧹 Módulo de Correção de Dados
Responsável por limpar e corrigir dados brutos recebidos. Ele detecta colunas desorganizadas e tenta reorganizá-las automaticamente com base em padrões aprendidos por modelos de IA.

---

### 🧠 Módulo de Criação de Modelos
Este módulo treina um classificador (ex: `RandomForestClassifier`) com os dados preparados. Ele gera um modelo que pode ser reutilizado para prever e corrigir novos dados.

---

### 🔍 Módulo de Predição
Com um modelo treinado, esta etapa permite a correção e classificação automática de novos dados. Os resultados são exibidos na interface e podem ser salvos no banco de dados MySQL.

---

### 💾 Banco de Dados
Todos os dados corrigidos podem ser armazenados no banco MySQL, facilitando o gerenciamento e uso posterior.

---

### 🖼️ Interface Web
Utilizamos **Streamlit** para criar uma interface amigável para o usuário, com:
- Correção de dados visual
- Armazenamento no banco
- Visualização dos resultados
""")

# Observação final
st.info("ℹ️ Observação: O projeto foi desenvolvido por alunos do primeiro semestre e possui foco educacional. Algumas funcionalidades estão em fase inicial e podem ser aprimoradas no futuro.")
