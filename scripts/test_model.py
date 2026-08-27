import ollama

response = ollama.chat(
    model="qwen2.5:7b",
    messages=[
        {
            "role": "user",
            "content": "Explain in 3 lines what an approval note is in a refinery."
        }
    ]
)

print(response["message"]["content"])