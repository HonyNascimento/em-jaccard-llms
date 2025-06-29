import ollama

# Nome do modelo que você já baixou (orc2)
model_name = "orca2"

# Prompt a ser enviado
prompt = "Do the following two product descriptions refer to the same item? " \
         "Product 1: Sony WH-1000XM4 Wireless Noise Cancelling Headphones. " \
         "Product 2: Sony Headphones WH1000XM4 with Noise Cancellation."

# Enviar o prompt para o modelo via Ollama
response = ollama.chat(
    model=model_name,
    messages=[
        {'role': 'user', 'content': prompt}
    ]
)

# Exibir a resposta
print(response['message']['content'])