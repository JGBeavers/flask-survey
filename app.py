from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
debug = DebugToolbarExtension(app)


responses = []

@app.route('/')
def home_page():
    return render_template('home_page.html', survey=survey)

@app.route('/questions/<int:id>')
def show_questions(id):

    question = survey.questions[id]

    return render_template('questions.html', survey=survey, question=question)