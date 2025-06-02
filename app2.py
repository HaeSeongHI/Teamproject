from flask import Flask, render_template, request
from openai import OpenAI
from pathlib import Path


app = Flask(__name__)

# API 클라이언트 설정
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="" ### API KEY 넣어라ㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏ
)


# 과목 정보 로딩
text_ac = Path('academic_en.txt')
text_ac_cont = text_ac.read_text(encoding='utf-8')



@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    user_input1 = ""
    user_input2 = ""
    user_input3 = ""
    
    if request.method == "POST":
        user_input1 = request.form["question1"]
        user_input2 = request.form["question2"]
        user_input3 = request.form["question3"]

        # 시스템 메시지 고정
        system_prompt = {
            'role': 'system',
            'content': 'You are a helpful, reasonable career counselor for university students. '
                    'You would recommend to students based on their basic informaton' + user_input1 + user_input2 + user_input3
        }

        system_prompt2 = {
            'role' : 'system', 'content': 'recommendation format would be: 1. REQUIRED course track, 2. RECOMMENDED course track, 3. Electives, 4. Additional acitivities to do, 5. Possible professions with these tracks'
        }

        system_prompt3 = {
            'role' : 'system', 'content' : 'You are going to be given the course details. Your recommendation should be in chronological order. For example, you can recommend like introduction to artificial intelligence and then machine learning since introduction to artificial intelligence is assigned at 1-1.' + text_ac_cont
        }

        messages = [system_prompt, system_prompt2, system_prompt3]
        
        try:
            completion = client.chat.completions.create(
                model="meta-llama/llama-3.3-70b-instruct:free",
                messages=messages
            )
            answer = completion.choices[0].message.content
        except Exception as e:
            answer = f"오류 발생: {str(e)}"

    return render_template("index.html", answer=answer, question1 = user_input1,
                                                        question2 = user_input2,
                                                        question3 = user_input3)

if __name__ == "__main__":
    app.run(debug=True)