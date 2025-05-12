import re
import pandas as pd
from datetime import datetime

def extract_features(X):
    """Extrai features para diversos tipos de dados brasileiros"""
    features = []
    for text in X:
        # Tratamento inicial do texto
        if pd.isna(text) or text == '':
            features.append({k: 0 for k in [
                'phone_score', 'email_score', 'age_score', 'address_score',
                'name_score', 'digit_count', 'special_char_count',
                'word_count', 'length', 'cpf_score', 'cnpj_score',
                'rg_score', 'cep_score', 'date_score'
            ]})
            continue
            
        text = re.sub(r'\s+', ' ', str(text).strip())
        words = text.split()
        digits = sum(c.isdigit() for c in text)
        special_chars = len(re.findall(r'[^a-zA-Z0-9\s]', text))
        
        feature_dict = {
            # Features originais
            'phone_score': int(bool(re.fullmatch(
                r'^(\+55\s?)?(\(?\d{2}\)?[\s-]?)?(\d{4,5}[\s-]?\d{4})$',
                text))) * 10,
            'email_score': int(bool(re.fullmatch(
                r'^[\w\.\+\-]+@[\w]+\.[a-z]{2,}(?:\.[a-z]{2})?$',
                text, flags=re.IGNORECASE))) * 10,
            'age_score': int(bool(re.fullmatch(
                r'^(1[01][0-9]|120|[1-9][0-9]|[0-9])$',
                text))) * 10,
            'address_score': (
                sum(1 for p in ['rua', 'av', 'avenida', 'travessa', 'alameda', 
                               'praça', 'rodovia', 'estrada', 'vl', 'vila']
                    if p in text.lower()) +
                (1 if re.search(r'\d{5}-?\d{3}', text) else 0) +
                (1 if len(text) > 15 and digits > 0 else 0)),
            'name_score': (
                3 if (len(words) in (2, 3) and text.istitle() and not digits and
                     not any(w.lower() in ['de', 'da', 'do', 'dos', 'das'] 
                            for w in words)) else 0),
            'digit_count': digits,
            'special_char_count': special_chars,
            'word_count': len(words),
            'length': len(text),
            
            # Novas features
            'cpf_score': int(bool(re.fullmatch(
                r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$',
                text))) * 10,
            'cnpj_score': int(bool(re.fullmatch(
                r'^\d{2}\.?\d{3}\.?\d{3}/\d{4}-?\d{2}$',
                text))) * 10,
            'rg_score': int(bool(re.fullmatch(
                r'^\d{1,2}\.?\d{3}\.?\d{3}-?[0-9A-Za-z]$',
                text))) * 10,
            'cep_score': int(bool(re.fullmatch(
                r'^\d{5}-?\d{3}$',
                text))) * 10,
            'date_score': int(bool(re.fullmatch(
                r'^\d{2}[/-]\d{2}[/-]\d{4}$|^\d{4}[/-]\d{2}[/-]\d{2}$',
                text))) * 10
        }
        features.append(feature_dict)
    return pd.DataFrame(features)