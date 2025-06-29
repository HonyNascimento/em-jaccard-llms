import pandas as pd
import ollama
import os
import time
from tqdm import tqdm

def query_llm(model_name, prompt):
    response = ollama.chat(
        model=model_name,
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content'].strip()

def classify_prompt_response(response):
    response_clean = response.lower().strip()
    if "true" in response_clean and "false" not in response_clean:
        return 1
    elif "false" in response_clean and "true" not in response_clean:
        return 0
    else:
        return -1  # Incerteza ou erro

def apply_llm_to_dataset(input_csv, output_csv, model_name):
    df = pd.read_csv(input_csv)

    # Inicializa colunas se ainda não existem
    if 'llm_response' not in df.columns:
        df['llm_response'] = ''
    if 'predicted_label' not in df.columns:
        df['predicted_label'] = -1

    for idx, row in tqdm(df.iterrows(), total=len(df), desc=f"Processando com {model_name}"):
        if row['predicted_label'] != -1:
            continue  # Pular se já processado

        prompt = row['prompt']
        try:
            response = query_llm(model_name, prompt)
            prediction = classify_prompt_response(response)
        except Exception as e:
            print(f"Erro com prompt: {prompt[:60]}... => {e}")
            response = "ERROR"
            prediction = -1

        df.at[idx, 'llm_response'] = response
        df.at[idx, 'predicted_label'] = prediction

        # Salvamento parcial a cada 50 linhas
        if idx % 50 == 0:
            df.to_csv(output_csv, index=False)

    # Salvamento final
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"Resultados salvos em: {output_csv}")


if __name__ == '__main__':
    models = ['orca2', 'zephyr']
    datasets = [
        ('data/abt_buy_prompts_zero_shot.csv', 'results/abt_buy_{model}_zero_shot.csv'),
        ('data/abt_buy_prompts_few_shot.csv', 'results/abt_buy_{model}_few_shot.csv'),
        ('data/walmart_amazon_prompts_zero_shot.csv', 'results/walmart_amazon_{model}_zero_shot.csv'),
        ('data/walmart_amazon_prompts_few_shot.csv', 'results/walmart_amazon_{model}_few_shot.csv')
    ]

    for model in models:
        for input_path, output_path_template in datasets:
            output_path = output_path_template.format(model=model)
            print(f"\nRodando modelo {model} para {input_path}...")
            start = time.time()
            try:
                apply_llm_to_dataset(input_path, output_path, model)
            except FileNotFoundError:
                print(f"Arquivo não encontrado: {input_path}. Pulando...")
            elapsed = time.time() - start
            print(f"Tempo de execução com {model}: {elapsed:.2f} segundos")
