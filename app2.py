from flask import Flask, render_template, request
from openai import OpenAI
from pathlib import Path


app = Flask(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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" ### API KEY is needed.
)


text_ac = Path('academic_en.txt')
text_ac_cont = text_ac.read_text(encoding='utf-8')



@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""             # get만 됐을때에도 render는 되기때문에 오류를 막으려면 기본값 넣어야함함
    user_input1 = ""
    user_input2 = ""
    user_input3 = ""
    user_input4 = ""
    
    if request.method == "POST":        # get인지 post인지
        user_input1 = request.form["question1"]
        user_input2 = request.form["question2"]
        user_input3 = request.form["question3"]
        user_input4 = request.form["question4"]

        system_prompt1 = 'You are a helpful, reasonable career counselor for university students.\
                    You would recommend to students based on their basic informaton'

        system_prompt2 ='recommendation format would be: \
                1. RECOMMENDED course track (It should be based on the text given), \
                2. REQUIRED course track for 1(Prerequisites and co-requisites should be considered and please note or show that which course is the prerequisite for which course.), \
                3. Additional acitivities to do, \
                4. Possible professions with these tracks'

        system_prompt3 ='You are going to be given the course details. Your recommendation should be in chronological order. \
                For example, you can recommend like introduction to artificial intelligence and then machine learning since introduction to artificial intelligence is assigned at 1-1.'



        user_input_all = f'This is a match between questions and user\'s answers to those questions.\
                Do you have any fields you want to focus on? : {user_input1}\
                Do you have any subjects you want to focus on? : {user_input2}\
                Do you have specific dreams or goals via AI? : {user_input3}\
                Any additional information?: {user_input4}\
                '


        messages = [{'role': 'system',
            'content': (system_prompt1 +'\n\n' + system_prompt2 +'\n\n' + system_prompt3 +'\n\n' + text_ac_cont +'\n\n' + user_input_all)
            }]
        
        try:
            completion = client.chat.completions.create(
                model="meta-llama/llama-3.3-70b-instruct:free",
                messages=messages
            )
            answer = completion.choices[0].message.content
        except Exception as e:
            answer = f"error: {str(e)}"

    return render_template("index.html", answer=answer, question1 = user_input1,
                                                        question2 = user_input2,
                                                        question3 = user_input3,
                                                        question4 = user_input4
                                                        )

if __name__ == "__main__":
    app.run(debug=True)