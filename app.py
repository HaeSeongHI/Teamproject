from flask import Flask, render_template, request
from openai import OpenAI
from pathlib import Path


app = Flask(__name__)

# API 클라이언트 설정
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)


# 과목 정보 로딩
text_ac = Path('academic_en.txt')
text_ac_cont = text_ac.read_text(encoding='utf-8')

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
