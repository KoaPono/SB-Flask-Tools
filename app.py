from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

SESSION = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "bananas"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def show_survey_start_page():
    return render_template('survey.html', survey=survey)

@app.route('/start', methods=["POST"])
def go_to_questions():
    session[SESSION] = []
    return redirect('/question/0')

@app.route('/question/<int:question_id>')
def show_question(question_id):
    responses = session[SESSION]
    if (len(responses) != question_id):
        flash(f"You are trying to access an invalid question")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[question_id]
    return render_template('question.html', question_id=question_id, question=question)

@app.route('/answer', methods=["POST"])
def redirect_to_questions():
    responses = session[SESSION]
    choice = request.form['answer']
    responses.append(choice)
    session[SESSION] = responses
    
    if len(responses) == len(survey.questions):
        return redirect('/complete')
    return redirect(f'/question/{len(responses)}')

@app.route('/complete')
def complete():
    return render_template('completion.html')