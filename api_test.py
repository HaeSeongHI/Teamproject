from openai import OpenAI
from pathlib import Path





pi_file = Path('academic.txt')
contents = pi_file.read_text(encoding = 'UTF-8')


client = OpenAI(
base_url="https://openrouter.ai/api/v1",
api_key="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",
)

completion = client.chat.completions.create(
model="meta-llama/llama-3.3-8b-instruct:free",
messages=[
    {
    "role": "user",
    "content": 'hi'
    }
]
)
print(completion.choices[0].message.content)