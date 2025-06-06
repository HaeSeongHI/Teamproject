from flask import Flask, render_template, request, session
from openai import OpenAI
from pathlib import Path


app = Flask(__name__)
app.secret_key = 'your_secret_key'

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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" ### API KEY is needed.
)


text_ac = Path('academic_en.txt')
text_ac_cont = text_ac.read_text(encoding='utf-8')
text_bc = Path('Best_Example.txt')
text_bc_cont = text_bc.read_text(encoding = 'utf-8')


def find_subject(subject):
    academis_splited = text_ac_cont.split('\n\n')
    for i in academis_splited:
        if 'Course title: '+subject in i:
            return i
    return 'not found'

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""             # get만 됐을때에도 render는 되기때문에 오류를 막으려면 기본값 넣어야함
    user_input1 = ""
    user_input2 = ""
    user_input3 = ""
    user_input4 = ""
    search_input = ""
    search_result = ""
    form_id = request.form.get("form_id")
    if request.method == "POST":        # get인지 post인지
        if form_id == 'form1':
            user_input1 = request.form["question1"]
            user_input2 = request.form["question2"]
            user_input3 = request.form["question3"]
            user_input4 = request.form["question4"]


            system_prompt1 = 'You are a helpful, reasonable career counselor for university students.\
                        You would recommend to students based on their basic informaton'

            system_prompt2 ='recommendation format would be: \
                    1. RECOMMENDED specific course track (It should be based on the text given), \
                    2. REQUIRED course track for 1(Prerequisites and co-requisites should be considered and please note or show that which course is the prerequisite for recommended course.), \
                    3. Additional acitivities to do, \
                    4. Possible professions with these tracks'

            system_prompt3 ='You are going to be given the course details. Your recommendation should be in chronological order. \
                    For example, you can recommend like introduction to artificial intelligence and then machine learning since introduction to artificial intelligence is assigned at 1-1.'
            
            system_prompt4 = 'Following statements are examples: ' + text_bc_cont

            user_input_all = f'This is a match between questions and user\'s answers to those questions.\
                    Do you have any fields you want to focus on? : {user_input1}\
                    Do you have any subjects you want to focus on? : {user_input2}\
                    Do you have specific dreams or goals via AI? : {user_input3}\
                    Any additional information?: {user_input4}\
                    '


            system_prompt5 = 'I want to recieve a list of recommended subjects on 1. So all you have to do is to add \
                "vrfctncdfspltng subjectname1,subjectname2,subjectname3....." on the last of your answer.\
                I am going to split your message and split by vrfctncdfspltng.\
                '


            messages = [{'role': 'system',
                'content': (system_prompt1 +'\n\n' + system_prompt2 +'\n\n' + system_prompt3 +'\n\n' + system_prompt4 + '\n\n'+ system_prompt5 + '\n\n' + text_ac_cont +'\n\n' + user_input_all)
                }]
            
            try:
                subjects_list = []
                completion = client.chat.completions.create(
                    model="meta-llama/llama-3.3-70b-instruct:free",
                    messages=messages
                )
                answer = completion.choices[0].message.content
                
                # 데이터랑 answer 분류
                subjects_list = answer.split('vrfctncdfspltng')[1]
                answer = answer.split('vrfctncdfspltng')[0]
                
                # 과목데이터 -> subjects_llist
                subjects_list = subjects_list.split(',')
                subjects_list = [i.strip() for i in subjects_list]
                
                subject_indexed = 'Recommended subjects: '
                for i in range(len(subjects_list)):
                    subject_indexed += f'\n{i+1}. {subjects_list[i]}'

                answer += '\n\n\n' + subject_indexed

                # session - 처음 go for it을 할 때 도출되었던 결과 저장 및 나중에 최종적으로 출력
                session['answer'] = answer
                session['user_input1'] = user_input1
                session['user_input2'] = user_input2
                session['user_input3'] = user_input3
                session['user_input4'] = user_input4
                session['search_result'] = search_result
                session['search_input'] = search_input
                session['subjects_list'] = subjects_list


            except Exception as e:
                answer = f"error: {str(e)}"

            
            return render_template("index.html", answer=answer, question1 = user_input1,
                                            question2 = user_input2,
                                            question3 = user_input3,
                                            question4 = user_input4,
                                            search_result= search_result,
                                            search_input = search_input
                                            )

        elif form_id == 'form2':
            # search box
            try:

                # -> 여기서 session에 저장되었던 것 출력
                answer = session.get('answer', '')

                user_input1 = session.get('user_input1', '')
                user_input2 = session.get('user_input2', '')
                user_input3 = session.get('user_input3', '')
                user_input4 = session.get('user_input4', '')
                
                search_result = session.get('search_result', [])
                search_input = session.get('search_input', [])
                subjects_list = session.get('subjects_list', [])
                
                search_input = request.form["search_subject"]
                search_result = find_subject(subjects_list[int(search_input)-1])
            except Exception as e:
                search_result = f"error: {str(e)}"

            return render_template("index.html", answer=answer, question1 = user_input1,
                                            question2 = user_input2,
                                            question3 = user_input3,
                                            question4 = user_input4,
                                            search_result= search_result,
                                            search_input = search_input
                                            )    
    
    # get일 때
    return render_template("index.html", answer=answer, question1 = user_input1,
                                            question2 = user_input2,
                                            question3 = user_input3,
                                            question4 = user_input4,
                                            search_result= search_result,
                                            search_input = search_input
                                            )

if __name__ == "__main__":
    app.run(debug=True)