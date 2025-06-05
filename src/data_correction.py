import pandas as pd
import joblib
import re
from pathlib import Path
from src.features import extract_features 

def formatar_telefone(tel):
    """Formata números de telefone brasileiros"""
    if pd.isna(tel) or not str(tel).strip():
        return None
    
    tel = re.sub(r'[^\d+]', '', str(tel))
    
    if len(tel) in (8, 9) and not tel.startswith(('0', '55', '+55')):
        if len(tel) == 8:
            return f"{tel[:4]}-{tel[4:]}"
        return f"{tel[:5]}-{tel[5:]}"
    
    if tel.startswith('55') and len(tel) > 11:
        tel = tel[2:]
    elif tel.startswith('+55') and len(tel) > 12:
        tel = tel[3:]
    
    if len(tel) == 11:
        return f"({tel[:2]}) {tel[2:7]}-{tel[7:]}"
    elif len(tel) == 10:
        return f"({tel[:2]}) {tel[2:6]}-{tel[6:]}"
    elif len(tel) == 9:
        return f"{tel[:5]}-{tel[5:]}"
    elif len(tel) == 8:
        return f"{tel[:4]}-{tel[4:]}"
    
    return tel

def formatar_documento(valor, tipo):
    """Formata CPF, CNPJ, RG e CEP"""
    if pd.isna(valor):
        return None
    
    valor = re.sub(r'[^\d]', '', str(valor))
    
    if tipo == 'CPF':
        return f"{valor[:3]}.{valor[3:6]}.{valor[6:9]}-{valor[9:]}" if len(valor) == 11 else valor
    elif tipo == 'CNPJ':
        return f"{valor[:2]}.{valor[2:5]}.{valor[5:8]}/{valor[8:12]}-{valor[12:]}" if len(valor) == 14 else valor
    elif tipo == 'RG':
        return f"{valor[:2]}.{valor[2:5]}.{valor[5:8]}-{valor[8:]}" if len(valor) >= 8 else valor
    elif tipo == 'CEP':
        return f"{valor[:5]}-{valor[5:]}" if len(valor) == 8 else valor
    return valor

def classificar_com_regras(valor, classe_predita, confianca):
    """Aplica regras adicionais para melhorar a classificação"""
    valor = str(valor).strip()
    
    # Ordem de prioridade das regras
    if re.fullmatch(r'^[\w\.\+\-]+@[\w]+\.[a-z]{2,}(?:\.[a-z]{2})?$', valor, re.IGNORECASE):
        return 'Email'
    
    if re.fullmatch(r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$', valor):
        return 'CPF'
    
    if re.fullmatch(r'^\d{2}\.?\d{3}\.?\d{3}/\d{4}-?\d{2}$', valor):
        return 'CNPJ'
    
    if re.fullmatch(r'^(\+55\s?)?(\(?\d{2}\)?[\s-]?)?(\d{4,5}[\s-]?\d{4})$', valor):
        return 'Telefone'
    
    if re.fullmatch(r'^\d{5}-?\d{3}$', valor):
        return 'CEP'
    
    if re.fullmatch(r'^\d{1,2}\.?\d{3}\.?\d{3}-?[0-9A-Za-z]$', valor):
        return 'RG'
    
    if re.fullmatch(r'^(1[01][0-9]|120|[1-9][0-9]|[0-9])$', valor):
        return 'Idade'
    
    if re.fullmatch(r'^\d{2}[/-]\d{2}[/-]\d{4}$|^\d{4}[/-]\d{2}[/-]\d{2}$', valor):
        return 'Data_Nascimento'
    
    if any(p in valor.lower() for p in ['rua', 'av', 'avenida', 'travessa', 'alameda', 'rodovia']):
        return 'Endereco'
    
    if confianca < 0.6:
        words = valor.split()
        if (len(words) in (2, 3) and valor.istitle() and 
            not any(c.isdigit() for c in valor) and
            not any(w.lower() in ['de', 'da', 'do'] for w in words)):
            return 'Nome'
    
    return classe_predita

def corrigir_dados(df, modelo):
    """Corrige dados bagunçados usando o modelo + regras"""
    colunas_saida = [
        'id', 'Nome', 'CPF', 'CNPJ', 'RG', 'CEP', 'Email', 
        'Telefone', 'Endereco', 'Data_Nascimento', 'Idade'
    ]
    dados_corrigidos = []
    todas_colunas = set()  # Para armazenar todas as colunas não nulas encontradas
    
    for _, linha in df.iterrows():
        registro = {col: None for col in colunas_saida}
        registro['id'] = linha.get('id', None)
        
        # Coletar valores não vazios (exceto ID)
        valores = [str(linha[col]).strip() for col in df.columns 
                 if col != 'id' and str(linha[col]).strip()]
        
        print(f"\nProcessando linha ID {linha['id']}: {valores}")
        
        if valores:
            try:
                # Extrair features
                features = extract_features(valores)
                
                # Verificar compatibilidade de features
                if hasattr(modelo, 'feature_names_in_'):
                    missing = set(modelo.feature_names_in_) - set(features.columns)
                    if missing:
                        for f in missing:
                            features[f] = 0
                    features = features[modelo.feature_names_in_]
                
                # Obter predições
                probas = modelo.predict_proba(features)
                classes = modelo.classes_
                
                for i, valor in enumerate(valores):
                    classe_idx = probas[i].argmax()
                    classe_predita = classes[classe_idx]
                    confianca = probas[i][classe_idx]
                    
                    classe_final = classificar_com_regras(valor, classe_predita, confianca)
                    
                    print(f"Valor: '{valor}' | Predito: {classe_predita} | Final: {classe_final} (conf: {confianca:.2f})")
                    
                    # Atribuir ao registro se o campo estiver vazio
                    if registro[classe_final] is None:
                        if classe_final == 'Telefone':
                            registro['Telefone'] = formatar_telefone(valor)
                        elif classe_final in ['CPF', 'CNPJ', 'RG', 'CEP']:
                            registro[classe_final] = formatar_documento(valor, classe_final)
                        elif classe_final == 'Email':
                            registro['Email'] = valor.lower()
                        elif classe_final == 'Idade':
                            registro['Idade'] = int(valor) if valor.isdigit() else None
                        else:
                            registro[classe_final] = valor
                
                # Verificação de conflitos
                for campo in ['Email', 'Telefone', 'CPF', 'CNPJ', 'RG', 'CEP']:
                    if registro[campo] and any(registro[campo] in str(v) for k,v in registro.items() if k != campo):
                        registro[campo] = None
                
                # Correção especial para telefones classificados como idade
                if not registro['Telefone'] and registro['Idade'] and len(str(registro['Idade'])) >= 8:
                    registro['Telefone'] = formatar_telefone(registro['Idade'])
                    registro['Idade'] = None
                    
            except Exception as e:
                print(f"Erro ao processar linha {linha['id']}: {str(e)}")
        
        registro_filtrado = {k: v for k, v in registro.items() if v is not None}
        dados_corrigidos.append(registro_filtrado)
        todas_colunas.update(registro_filtrado.keys())  # Adiciona as colunas encontradas
        
    # Converte para DataFrame e ordena as colunas
    df_corrigido = pd.DataFrame(dados_corrigidos)
    colunas_ordenadas = [col for col in colunas_saida if col in todas_colunas]
    
    return df_corrigido, colunas_ordenadas

def run_data_correction(input_path, model_path):
    try:
        # 1. Carregar modelo e dados
        modelo = joblib.load(model_path)
        df = pd.read_csv(input_path)
        
        # 2. Processar dados
        df_corrigido, colunas_nao_nulas = corrigir_dados(df, modelo)
        
        # 3. Garantir todas as colunas de saída (na ordem original)
        colunas_saida = colunas_nao_nulas
        print(f"Colunas não nulas encontradas: {colunas_saida}")
        
        # Adiciona colunas faltantes
        for col in colunas_saida:
            if col not in df_corrigido:
                df_corrigido[col] = None
        
        # Ordena colunas conforme a ordem definida
        df_corrigido = df_corrigido[colunas_saida]
        
        # 4. Definir caminho fixo para saída
        output_dir = Path("data/output")
        output_dir.mkdir(parents=True, exist_ok=True)  # Cria a pasta se não existir
        
        # Mantém o nome do arquivo original (ou usa um padrão, como "dados_corrigidos.csv")
        output_file = output_dir / Path(input_path).name  # Ex: "dados.csv" → "/home/.../output/dados.csv"
        
        df_corrigido.to_csv(output_file, index=False)
        print(f"Dados corrigidos salvos em: {output_file}")
        
        return True, output_file
    
    except Exception as e:
        print(f"Erro durante a correção: {str(e)}")
        return False

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Caminho para dados de entrada')
    parser.add_argument('--model', required=True, help='Caminho para o modelo')
    parser.add_argument('--output', required=True, help='Caminho para salvar resultados')
    args = parser.parse_args()
    
    run_data_correction(args.input, args.model, args.output)

# if __name__ == '__main__':
#     try:
#         # 1. Carregar modelo
#         modelo = joblib.load("modelo_classificador_completo.joblib")
#         print("Modelo carregado com sucesso!")
        
#         # 2. Carregar dados
#         df = pd.read_csv("/home/victor/workspace/Fabrica_Projetos/data/dados_bagunçados.csv")
#         print(f"\nDados carregados: {len(df)} registros")
        
#         # 3. Corrigir dados (agora recebemos ambos valores)
#         df_corrigido, colunas_nao_nulas = corrigir_dados(df, modelo)
 
#         # 4. Garantir todas as colunas de saída
#         for col in colunas_nao_nulas:
#             if col not in df_corrigido:
#                 df_corrigido[col] = None
        
#         # 5. Ordenar colunas conforme colunas_nao_nulas
#         df_corrigido = df_corrigido[colunas_nao_nulas]
        
#         # 6. Salvar resultados
#         df_corrigido.to_csv("dados_corrigidos_final.csv", index=False)
#         print("\nDados salvos em 'dados_corrigidos_final.csv'")
        
#     except Exception as e:
#         print(f"\nErro: {str(e)}")
#         exit(1)