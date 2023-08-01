from flask import Flask, request, render_template, redirect, flash, jsonify, current_app, session
from random import randint, choice, sample
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

RESPONSES_KEY = "responses" 
# 1

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Milo2011'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []
global_id = [0]



@app.route('/')
def home_page():
    """ shows home page"""
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    questions = satisfaction_survey.questions
    session[RESPONSES_KEY] = []
    # 2
    return render_template('home.html', title = title, instructions = instructions, questions = questions)

@app.route('/questions/<int:qid>', methods=['POST', 'GET'])
def questions(qid):
    """render questions"""
    for num in global_id:
        val = int(num)
        if val == qid:
            if request.method== 'GET':
                question = satisfaction_survey.questions[qid]
                return render_template('questions.html', question = question, qid=qid)
            elif request.method == 'POST':
                answer = request.form['answer']
                responses = session[RESPONSES_KEY]
                # 3
                responses.append(answer)
                session[RESPONSES_KEY] = responses
                # 4
                print('**************')
                print(responses)
                print('**************')
                global_id[0] += 1
                if global_id[0] > 3:
                    global_id[0] = 0
                    return redirect('/answers')
                else:
                    print('**************')
                    print(responses)
                    print('**************')
                    return redirect(f'/questions/{global_id[0]}')
        elif val != qid:
            flash('You must answer the questions in order!')
            return redirect(f'/questions/{val}')



@app.route('/thank-you')
def thanks():
    """ thank the surveyor"""
    return render_template('thank_you.html')

@app.route('/answers', methods=['GET'])
def display_answers():
    """display answere"""
    responses = session.get(RESPONSES_KEY)
    return render_template('answers.html', responses = responses)

@app.route('/answers/new', methods=['POST'])
def collect_answers():
    """collect answers"""
    return render_template('/answers')
