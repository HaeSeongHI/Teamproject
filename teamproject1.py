from openai import OpenAI
from pathlib import Path

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

messages = [{'role':'system', 'content':text}]


completion = client.chat.completions.create(

  model="meta-llama/llama-3.3-70b-instruct:free",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)
print(completion.choices[0].message.content)

print("hello")