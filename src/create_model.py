# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import FunctionTransformer
# import joblib
# from .features import extract_features

# # 1. Carregar dados de treino (agora com exemplos de CPF, CNPJ, etc.)
# df = pd.read_csv("/home/victor/workspace/Fabrica_Projetos/data/dataset_treino_br.csv")  # Seu dataset deve conter exemplos variados

# # 2. Verificar balanceamento
# print("Distribuição original:")
# print(df['tipo'].value_counts())

# # 3. Pré-processamento
# X = df['valor']
# y = df['tipo']

# # 4. Dividir dados
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42, stratify=y)

# # 5. Pipeline com mais árvores para lidar com mais classes
# pipeline = Pipeline([
#     ('features', FunctionTransformer(extract_features)),
#     ('classifier', RandomForestClassifier(
#         n_estimators=500,
#         class_weight='balanced',
#         max_depth=15,
#         random_state=42,
#         min_samples_leaf=3
#     ))
# ])

# # 6. Treinar
# pipeline.fit(X_train, y_train)

# # 7. Avaliar
# from sklearn.metrics import classification_report
# print("\nRelatório de classificação:")
# print(classification_report(y_test, pipeline.predict(X_test)))

# # 8. Salvar novo modelo
# joblib.dump(pipeline, "modelo_classificador_completo.joblib")
# print("\nNovo modelo treinado e salvo com sucesso!")

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
import joblib
from src.features import extract_features 
from sklearn.metrics import classification_report


def create_model():
    
    # 1. Carregar dados de treino
    df = pd.read_csv("/home/victor/workspace/Fabrica_Projetos/data/dataset_treino_br.csv")

    # 2. Verificar balanceamento
    print("Distribuição original:")
    print(df['tipo'].value_counts())

    # 3. Pré-processamento
    X = df['valor']
    y = df['tipo']

    # 4. Dividir dados
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    # 5. Pipeline
    pipeline = Pipeline([
        ('features', FunctionTransformer(extract_features)),
        ('classifier', RandomForestClassifier(
            n_estimators=500,
            class_weight='balanced',
            max_depth=15,
            random_state=42,
            min_samples_leaf=3
        ))
    ])

    # 6. Treinar
    pipeline.fit(X_train, y_train)

    # 7. Avaliar
    print("\nRelatório de classificação:")
    print(classification_report(y_test, pipeline.predict(X_test)))

    # 8. Salvar modelo
    joblib.dump(pipeline, "modelo_classificador_completo.joblib")
    print("\nNovo modelo treinado e salvo com sucesso!")


if __name__ == "__main__":
    create_model()
