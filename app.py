from flask import Flask, render_template, request
from openai import OpenAI
from pathlib import Path
import os

app = Flask(__name__)

# API 클라이언트 설정
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=""
)


# 과목 정보 로딩
text_ac = Path('academic.txt')
text_ac_cont = text_ac.read_text(encoding='utf-8')

# AI에 관한 흥미?
ans1 = input("Are you interested in Artificial Intelligence?: ")

# 공부하고 싶은 분야?
ans2 = input("Do you have any fields that you want to focus on?: ")

# 흥미있는 과목?
ans3 = input("Do you have any subjects that you want to focus on?: ")

# 생각중인 진로?
ans4 = input("Do you have specific dreams or goals that you want to achieve via AI?: ")

# 시스템 메시지 고정
system_prompt = {
    'role': 'system',
    'content': 'You are a helpful, reasonable career counselor for university students. '
            'You would recommend to students about what subjects(only from a text given) would be better for them to take '
            'in terms of their preference and talents.'
            'Also you can teach user what subject should be preceded,'
            'or future career related to reccomended subject.'
            'Respond and explain about subjects specifically based on following text.'+ text_ac_cont
}

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    user_input = ""

    if request.method == "POST":
        user_input = request.form["question"]
        messages = [system_prompt, {'role': 'user', 'content': user_input + "(Recommand some subjects for me.)"}]
        
        try:
            completion = client.chat.completions.create(
                model="meta-llama/llama-3.3-70b-instruct:free",
                messages=messages
            )
            answer = completion.choices[0].message.content
        except Exception as e:
            answer = f"오류 발생: {str(e)}"

    return render_template("index.html", answer=answer, question=user_input)

if __name__ == "__main__":
    app.run(debug=True)
