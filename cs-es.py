from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import json
import os

with open(os.path.join(os.path.dirname(__file__), 'db.json'), encoding='utf-8') as f:
    data = json.load(f)

app = Flask(__name__)

student_info = {
    "Name": ""
}

curr_question = list(data.keys())[0]
curr_response = data[curr_question]
last_q = []
last_r = curr_response
final_answer = ""

# Begin
@ app.route('/')
def home():
    curr_time = datetime.now()
    hour = int(curr_time.strftime("%H"))

    if hour >= 0 and hour < 12:
        message = "Morning"
    elif hour >= 12 and hour < 17:
        message = "Afternoon"
    else:
        message = "Evening"

    return render_template("home.html", message=message)


@ app.route("/get-to-know", methods=["GET", "POST"])
def get_info():
    if request.method == "POST":
        student_info["Name"] = request.form["name"]
        return redirect("/get-to-know/introduction")

    return render_template("information.html")

# main
@ app.route("/get-to-know/introduction", methods=["GET", "POST"])
def intro():
    if request.method == "POST":
        response = request.form["response-button"]

        global curr_response
        global curr_question
        global last_q
        global last_r

        last_q = []

        next_decision = curr_response[response]
        question = list(next_decision.keys())[0]
        next_responses = next_decision[question]
        curr_response = next_responses
        curr_question = question
        last_q.append(curr_question)
        last_r = curr_response

        return redirect("/get-to-know/introduction/question")

    else:
        responses = list(curr_response.keys())
        return render_template("introduction.html", name=student_info["Name"], main_question=curr_question, responses=responses)


@ app.route("/get-to-know/introduction/question", methods=["GET", "POST"])
def questions():
    if request.method == "POST":
        try:
            global last
            response = request.form["response-button"]

        except KeyError:
            curr_question = list(data.keys())[0]
            curr_response = data[curr_question]
            return redirect('/get-to-know/introduction')
        
        else:
            global curr_response
            global curr_question
            global final_answer
            global last_r

            next_decision = curr_response[response]

            if isinstance(next_decision, dict):
                question = list(next_decision.keys())[0]
                curr_question = question
                next_responses = next_decision[question]
                curr_response = next_responses
                last_q.append(curr_question)
                last_r = curr_response

                return render_template("questions.html", main_question=question, responses=next_responses)
            else:
                curr_question = response
                final_answer = next_decision
                last_q.append(curr_question)
                return redirect("/get-to-know/introduction/question/answer")

    return render_template("questions.html", main_question=curr_question, responses=curr_response)


@ app.route("/get-to-know/introduction/question/answer", methods=["GET", "POST"])
def answer():
    if request.method == "POST":

        global curr_question
        global curr_response
        global last_q
        global last_r

        print(last_q)
        last_q.pop()
        curr_question = last_q[-1]
        curr_response = last_r

        return redirect('/get-to-know/introduction/question')

    if "question" in request.args:
        return render_template("answer.html", question=request.args["question"], answer=request.args["answer"])
    return render_template("answer.html", question=curr_question, answer=final_answer)

app.run(debug=True)

# Test
@ app.route("/get-to-know/introduction/question/test", methods=["GET", "POST"])
def test():
    pass
