from openai import OpenAI
from pathlib import Path

text_ac = Path('academic.txt')
text_ac_cont = text_ac.read_text(encoding='utf-8')

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="",
)

messages = [{'role':'system', 'content': 'You are an helpful, reasonable career counselor for university students. You would recommend to students about what subjects would be better for them to take in terms of their preference and talents.' + text_ac_cont}]

while True:
  msg = input('Are you curious about your future? I will tell you what to do: ')
  messages.append({'role':'user', 'content':msg})
  completion = client.chat.completions.create(

    model="meta-llama/llama-3.3-70b-instruct:free",
    messages = messages
  )
  print(completion.choices[0].message.content)
  messages.append(completion.choices[0].message)