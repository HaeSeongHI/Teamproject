from openai import OpenAI

client = OpenAI(
base_url="https://openrouter.ai/api/v1",
api_key="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",
)

completion = client.chat.completions.create(
model="meta-llama/llama-3.3-8b-instruct:free",
messages=[
    {
    "role": "user",
    "content": "What is the meaning of life?"
    }
]
)
print(completion.choices[0].message.content)