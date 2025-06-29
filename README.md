# Entity Matching with 7B LLMs (Reprodução)

Este repositório contém a reprodução parcial do artigo **“Entity Matching with 7B LLMs: A Study on Prompting Strategies and Hardware Limitations”**, com foco na aplicação de **modelos LLM de 7 bilhões de parâmetros** (notadamente **Orca2**) para a tarefa de *entity matching* utilizando **prompting zero-shot e few-shot**.

> 🔬 Esta reprodução foi realizada com recursos computacionais limitados e teve como principal objetivo verificar a reprodutibilidade dos resultados do artigo original utilizando o dataset **Abt-Buy**.

## 📁 Estrutura do Repositório

```
.
├── data/                  # Datasets e arquivos de prompt
│   ├── Abt.csv
│   ├── Buy.csv
│   ├── abt_buy_perfectMapping.csv
│   └── ...                # Arquivos de prompt gerados
├── results/               # Resultados das execuções com LLMs
├── scripts/               # Scripts Python organizados por etapa
│   ├── 1_generate_pairs.py
│   ├── 2_generate_prompts.py
│   ├── 3_apply_llm.py
│   ├── 4_evaluate_results.py
│   └── utils.py           # Funções auxiliares
└── README.md
```

## 📦 Datasets

Os datasets utilizados foram:

- **Abt-Buy**:
[Link](https://paperswithcode.com/dataset/abt-buy)
[Download direto](https://dbs.uni-leipzig.de/files/datasets/Abt-Buy.zip)
- **Walmart-Amazon**:
[Link](https://www.kaggle.com/datasets/satriowp/amazonwalmart-dataset?resource=download&SSORegistrationToken=CfDJ8KT8tnOr7fFFm_byYmusL7h5Ty19or31iMUbEDc69D6JJj5V58Gr-d6lJ4HJkStuuZ8KpAqQ9GdoXf0FoxrVLXdroisIQzkqb7h8f-tke0w3X0fw8Kkim5FOpjR7wHrjPKlKPquGUQ27cGN1vR9NtC1uLmwvQ_ajiD6_eIlJkilQicMeK4bpcQxH9bdUEF1QrUDh1WdFniYvAAhL-BW53GkMXbeG7Uprj8uTxWybyalKY1oAL7q62gX1BosGDkmLqf_4Jm2hmtNM-KMwvja6wc8kBJ0eierSchIiiny0HYQWDp7NZvOdK7OtEgUefAXgAUlnkRm6cMoDT0_fWPA4HXM&DisplayName=Hony%20A%20Nascimento)

---

## 🚀 Como Executar

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

> Módulos principais: `pandas`, `tqdm`, `scikit-learn`, `ollama`

### 2. Prepare os pares de dados

```bash
python scripts/1_generate_pairs.py
```

### 3. Gere os prompts

```bash
python scripts/2_generate_prompts.py
```

### 4. Execute os modelos LLM

```bash
python scripts/3_apply_llm.py
```

> ⚠️ Tempo estimado para Orca2 zero-shot: ~21h com CPU; few-shot: ~32h

### 5. Avalie os resultados

```bash
python scripts/4_evaluate_results.py
```

## 📊 Resultados Obtidos

| Estratégia       | Fonte        | Precision | Recall | F1-score | Tempo Execução |
|------------------|--------------|-----------|--------|----------|----------------|
| Zero-shot        | Artigo       | 0.664     | 0.956  | 0.784    | -              |
| Zero-shot        | Reprodução   | 0.9971    | 0.6462 | 0.7842   | 20h 58min      |
| Few-shot (FT)    | Artigo       | 0.768     | 0.834  | 0.799    | -              |
| Few-shot (FT)    | Reprodução   | 1.0000    | 0.4000 | 0.5714   | 32h 27min      |

## ⚙️ Requisitos

- Python 3.13.3
- Ollama 0.9.2 com o modelo [Orca2](https://ollama.com/library/orca2) instalado
- Memória RAM recomendada: 16GB+
- Ambiente testado com CPU (i7-8750H) e GPU GTX 1050 (4GB)

Na primeira versão do experimento foi utilizado o seguinte hardware:
- Notebook Dell G7 15 7588 (SO Windows)
- Processador i7-8750H (2.20GHz)
- 16 GB de memória RAM 
- GPU NVIDIA GTX 1050 4GB


## 📌 Observações

- Devido a limitações de hardware, o dataset **Walmart-Amazon** não foi processado.
- Os exemplos few-shot utilizados foram **genéricos**, o que pode ter afetado o desempenho.
- O código está modularizado para permitir reuso e expansão em experimentos futuros.

## 📎 Referência Original

Arvanitis-Kasinikos, I., & Papadakis, G. (2025). *Entity Matching with 7B LLMs: A Study on Prompting Strategies and Hardware Limitations*. DOLAP 2025.
