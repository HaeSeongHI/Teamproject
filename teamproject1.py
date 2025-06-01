from openai import OpenAI
from pathlib import Path

text_ac = Path('academic.txt')
text_ac_cont = text_ac.read_text(encoding='utf-8')

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

messages = [{'role':'system', 'content': 'You are an helpful, reasonable advisor'}]

while True:
  msg = input('Are you curious about your future? I will tell you what to do ')
  messages.append({'role':'user', 'content':msg})
  completion = client.chat.completions.create(

    model="meta-llama/llama-3.3-70b-instruct:free",
    messages = messages
  )
  print(completion.choices[0].message.content)
  messages.append(completion.choices[0].message)