import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report
import os

def evaluate_predictions(csv_path):
    if not os.path.exists(csv_path):
        print(f"Arquivo não encontrado: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    df = df[df['predicted_label'] != -1]  # filtrar apenas os exemplos válidos

    if df.empty:
        print(f"Sem dados válidos para avaliar em {csv_path}")
        return

    y_true = df['is_match']
    y_pred = df['predicted_label']

    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    print(f"\nAvaliação para: {csv_path}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print("\nRelatório completo:\n")
    print(classification_report(y_true, y_pred))

if __name__ == '__main__':
    arquivos_resultados = [
        'results/abt_buy_orca2_zero_shot.csv',
        'results/abt_buy_orca2_few_shot.csv',
        'results/abt_buy_zephyr_zero_shot.csv',
        'results/abt_buy_zephyr_few_shot.csv',
        'results/walmart_amazon_orca2_zero_shot.csv',
        'results/walmart_amazon_orca2_few_shot.csv',
        'results/walmart_amazon_zephyr_zero_shot.csv',
        'results/walmart_amazon_zephyr_few_shot.csv'
    ]

    for resultado in arquivos_resultados:
        evaluate_predictions(resultado)
