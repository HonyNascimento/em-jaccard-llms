import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score
from tqdm import tqdm
import time


def jaccard_similarity(str1, str2):
    tokens1 = set(str(str1).lower().split())
    tokens2 = set(str(str2).lower().split())
    if not tokens1 or not tokens2:
        return 0.0
    return len(tokens1 & tokens2) / len(tokens1 | tokens2)

# Configurações dos experimentos
experiments = [
    {
        'input_file': 'data/abt_buy_pairs_labeled.csv',
        'name_col_1': 'name_abt',
        'name_col_2': 'name_buy',
        'output_file': 'data/abt_buy_jaccard_thresholds.csv'
    },
    {
        'input_file': 'data/walmart_amazon_pairs_labeled.csv',
        'name_col_1': 'title_x',
        'name_col_2': 'title_y',
        'output_file': 'data/walmart_amazon_jaccard_thresholds.csv'
    }
]

for exp in experiments:
    print(f"\nProcessando: {exp['input_file']}")
    df = pd.read_csv(exp['input_file'])

    print("Calculando similaridade de Jaccard...")
    df['score'] = [jaccard_similarity(row[exp['name_col_1']], row[exp['name_col_2']]) for _, row in tqdm(df.iterrows(), total=df.shape[0])]

    thresholds = [round(i * 0.1, 1) for i in range(1, 11)]
    results = []

    print("Avaliando thresholds...")
    for threshold in tqdm(thresholds):
        start_time = time.time()

        df['predicted'] = (df['score'] >= threshold).astype(int)
        y_true = df['is_match']
        y_pred = df['predicted']

        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        total_time = round(time.time() - start_time, 4)

        results.append({
            'threshold': threshold,
            'precision': round(precision, 4),
            'recall': round(recall, 4),
            'f1_score': round(f1, 4),
            'total_records': len(df),
            'predicted_matches': int((df['predicted'] == 1).sum()),
            'predicted_non_matches': int((df['predicted'] == 0).sum()),
            'execution_time_seconds': total_time
        })

    results_df = pd.DataFrame(results)
    results_df.to_csv(exp['output_file'], index=False)
    print(f"Resultados salvos em: {exp['output_file']}")
    print(results_df)
