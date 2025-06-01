from openai import OpenAI
from pathlib import Path





pi_file = Path('academic.txt')
contents = pi_file.read_text(encoding = 'UTF-8')


print(contents)