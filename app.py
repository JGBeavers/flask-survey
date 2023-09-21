from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
debug = DebugToolbarExtension(app)


responses = []

@app.route('/')
def home_page():
    """Display survey name and instructions and button to begin"""

    return render_template('home_page.html', survey=survey)

@app.route('/questions/<int:id>')
def show_questions(id):
    """Display current question using id and choices, send choice to /answer""" 

    if (len(responses) != id):
        flash(f"Invalid question id: {id}.")
        return redirect(f"/questions/{len(responses)}")

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")  
    
    question = survey.questions[id]

    return render_template('questions.html', survey=survey, question=question)

@app.route('/answer', methods=['POST'])
def get_answer():
    """Append choice to responses and redirect to next question"""

    choice = request.form['answer']
    responses.append(choice)

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    return redirect(f'/questions/{len(responses)}')

@app.route('/complete')
def survey_complete():
    """redirect to survey complete page when all questions answered"""

    return render_template('complete.html', survey=survey)