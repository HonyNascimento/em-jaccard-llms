import pandas as pd
import os

def generate_zero_shot_prompt(title_left, title_right):
    prompt = (
        "Do the following two product descriptions refer to the same real-world item?\n"
        f"Product 1: {title_left}\n"
        f"Product 2: {title_right}\n"
        "Respond with True or False."
    )
    return prompt


def generate_few_shot_prompt(title_left, title_right, example_true, example_false, order='TF'):
    true_example = (
        "Product 1: " + example_true[0] + "\n"
        "Product 2: " + example_true[1] + "\n"
        "Answer: True"
    )
    false_example = (
        "Product 1: " + example_false[0] + "\n"
        "Product 2: " + example_false[1] + "\n"
        "Answer: False"
    )

    examples = true_example + "\n\n" + false_example if order == 'TF' else false_example + "\n\n" + true_example

    task = (
        "Do the following two product descriptions refer to the same real-world item?\n"
        f"Product 1: {title_left}\n"
        f"Product 2: {title_right}\n"
        "Answer:"
    )

    return examples + "\n\n" + task


def generate_prompts_from_dataset(input_csv, output_csv, strategy='zero_shot', example_true=None, example_false=None, order='TF'):
    df = pd.read_csv(input_csv)

    prompts = []
    for _, row in df.iterrows():
        title_left = row.get('name_abt') or row.get('title_left') or row.get('title') or row.get('name_x')
        title_right = row.get('name_buy') or row.get('title_right') or row.get('title') or row.get('name_y')

        if strategy == 'zero_shot':
            prompt = generate_zero_shot_prompt(title_left, title_right)
        elif strategy == 'few_shot':
            if not example_true or not example_false:
                raise ValueError("Exemplos true/false devem ser fornecidos para few-shot prompting.")
            prompt = generate_few_shot_prompt(title_left, title_right, example_true, example_false, order)
        else:
            raise ValueError("Estratégia inválida. Use 'zero_shot' ou 'few_shot'.")

        prompts.append(prompt)

    df['prompt'] = prompts
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"Prompts salvos em: {output_csv}")


# Exemplo de uso:
if __name__ == '__main__':
    # Exemplos para few-shot (pode ser extraído do próprio dataset posteriormente)
    ex_true = ("Apple iPhone 13 128GB Blue", "iPhone 13 Apple Blue 128 GB")
    ex_false = ("Samsung Galaxy S22 Ultra 256GB", "Canon EOS Rebel T7 DSLR Camera")

    # Abt-Buy Zero-shot
    abt_input = 'data/abt_buy_pairs_labeled.csv'
    abt_output = 'data/abt_buy_prompts_zero_shot.csv'
    generate_prompts_from_dataset(abt_input, abt_output, strategy='zero_shot')

    # Abt-Buy Few-shot (opcional)
    abt_output_fs = 'data/abt_buy_prompts_few_shot.csv'
    generate_prompts_from_dataset(abt_input, abt_output_fs, strategy='few_shot', example_true=ex_true, example_false=ex_false, order='TF')

    # Walmart-Amazon Zero-shot
    wa_input = 'data/walmart_amazon_pairs_labeled.csv'
    wa_output = 'data/walmart_amazon_prompts_zero_shot.csv'
    generate_prompts_from_dataset(wa_input, wa_output, strategy='zero_shot')

    # Walmart-Amazon Few-shot (opcional)
    wa_output_fs = 'data/walmart_amazon_prompts_few_shot.csv'
    generate_prompts_from_dataset(wa_input, wa_output_fs, strategy='few_shot', example_true=ex_true, example_false=ex_false, order='TF')
