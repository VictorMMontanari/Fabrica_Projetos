# 🧼 DbClean — Ferramenta de Limpeza e Migração de Dados com IA

DbClean é uma ferramenta baseada em inteligência artificial, desenvolvida para **automatizar, limpar e organizar dados empresariais** durante processos de migração de sistemas.

## 📌 Visão Geral

O objetivo da ferramenta é substituir procedimentos manuais e suscetíveis a erros por um processo automatizado e inteligente, reduzindo **custos**, **tempo de execução** e **retrabalho** em ambientes corporativos.

---

## 🎯 Finalidade

DbClean busca tornar a migração de dados mais:

- ✅ Eficiente  
- ✅ Rápida  
- ✅ Segura

Utilizando algoritmos de **machine learning**, a ferramenta identifica padrões, corrige problemas estruturais e reorganiza os dados para ambientes modernos.

---

## ⚙️ Funcionalidades Implementadas

- ✔️ Correção de colunas desorganizadas com IA (`RandomForestClassifier`)
- ✔️ Interface visual com [Streamlit](https://streamlit.io/)
- ✔️ Armazenamento dos dados tratados em banco de dados **MySQL**

---

## 🖼️ Demonstração

### 📍 Tela Inicial da Interface

![Tela Inicial](https://raw.githubusercontent.com/VictorMMontanari/Fabrica_Projetos/refs/heads/main/utils/assets/tela_in.png)

---

### 🧠 Execução do Modelo IA

![Correção de Dados](https://raw.githubusercontent.com/VictorMMontanari/Fabrica_Projetos/refs/heads/main/utils/assets/Tela_IA.png)

---

### 🗃️ Envio ao MySQL

![MySQL Integração](https://raw.githubusercontent.com/VictorMMontanari/Fabrica_Projetos/refs/heads/main/utils/assets/tela_mysql.png)

---

## 🧪 Tecnologias Utilizadas

### 💻 Linguagem:
- Python 3.10+

### 📚 Bibliotecas:
- `pandas`
- `scikit-learn`
  - `RandomForestClassifier`, `Pipeline`, `FunctionTransformer`, `classification_report`
- `joblib`
- `Streamlit`
- `mysql-connector-python` ou `SQLAlchemy`

---

## 🧠 Sobre o Desenvolvimento

> **Importante**: Este projeto foi desenvolvido por alunos do **primeiro semestre da graduação**, ainda com conhecimentos introdutórios em programação, IA e banco de dados.

Todas as funcionalidades implementadas foram baseadas no conteúdo abordado em aula (especialmente na disciplina de **Introdução à Inteligência Artificial**, com o professor Henrique), complementadas com pesquisas próprias.

Apesar da limitação técnica do grupo, conseguimos entregar um sistema funcional com:

- Aprendizado de máquina real;
- Interface prática com Streamlit;
- Integração com MySQL;
- Estrutura modular do código.

---

## 🔜 Próximos Passos

- 🔄 Melhorar desempenho do modelo com novos dados
- 🧾 Adicionar validações e tratamento de erros
- 🧑‍💻 Autenticação e controle de acesso na interface
- ☁️ Deploy da aplicação em ambiente de produção (nuvem)
- 🧹 Suporte a formatos diversos (JSON, XML etc.)

