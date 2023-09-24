from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
debug = DebugToolbarExtension(app)


# responses = []

@app.route('/')
def home_page():
    """Display survey name and instructions and button to begin"""

    return render_template('home_page.html', survey=survey)

@app.route("/start", methods=["POST"])
def start_survey():
    """Clear the responses session"""

    session['responses'] = []

    return redirect("/questions/0")

@app.route('/questions/<int:id>')
def show_questions(id):
    """Display current question using id and choices, send choice to /answer"""
    responses = session.get('responses')

    if (responses is None):
        return redirect("/")

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
    responses = session['responses']
    responses.append(choice)
    session['responses'] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    return redirect(f'/questions/{len(responses)}')

@app.route('/complete')
def survey_complete():
    """redirect to survey complete page when all questions answered"""

    return render_template('complete.html', survey=survey)