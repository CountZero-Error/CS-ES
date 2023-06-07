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
            if response == "Develop you own cognitive science experiment.":
                return redirect("/get-to-know/introduction/question/test")

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

        if last_q[-1] == "Test":
            last_q.pop()
            redirect('/get-to-know/introduction')

        last_q.pop()
        curr_question = last_q[-1]
        curr_response = last_r

        return redirect('/get-to-know/introduction/question')

    if "question" in request.args:
        return render_template("answer.html", question=request.args["question"], answer=request.args["answer"])
    return render_template("answer.html", question=curr_question, answer=final_answer)

# Test
@ app.route("/get-to-know/introduction/question/test", methods=["GET", "POST"])
def test():
    global last_q
    last_q.append("Test")

    test_data = data["Do you have experience in cognitive science?"]["Yes"]["What would you like to know today?"]["Develop you own cognitive science experiment."]
    test_rules = []
    test_rules.extend(rule for rule in test_data["2"])
    test_rules.extend(rule for rule in test_data["3"])
    test_rules.extend(rule for rule in test_data["48"])
    test_rules.extend(rule for rule in test_data["5"])
    test_rules.extend(rule for rule in test_data["6"])
    test_rules.extend(rule for rule in test_data["7"])

    if request.method == "POST":
        rule_ans = request.form.to_dict()

        ans_text = {"2": "You can use methods like visual perception experiments or eye-tracking studies to explore how individuals perceive and interpret visual stimuli.",
                    "3": "You can consider using methods such as psycholinguistic experiments or language processing tasks to investigate the relationship between language and cognition.",
                    "48": "Methods like attentional tasks or memory experiments can help you examine how attention and memory interact during learning tasks and the role of problem-solving strategies in cognitive processes.",
                    "5": "You can explore using neuroimaging techniques like fMRI or EEG to study the neural mechanisms underlying cognitive processes.",
                    "6": "Methods such as emotional priming tasks or emotional memory experiments can be used to investigate the effect of emotions on cognitive performance.",
                    "7": "Methods like information processing tasks or perceptual experiments can help you study how people acquire and process information from the environment.",
                    'Not valid': 'There is no experiment that can fulfill your requirements. Please try again.',
                    None: "Please insert atleast one requirement and try again."}
        result_test = None
        for rule in test_rules:
            if rule_ans[rule] == "Yes":
                if rule in test_data["2"]:
                    if result_test is None:
                        result_test = "2"
                    elif result_test != "2":
                        result_test = 'Not valid'
                        break
                elif rule in test_data["3"]:
                    if result_test is None:
                        result_test = "3"
                    elif result_test != "3":
                        result_test = 'Not valid'
                        break
                elif rule in test_data["48"]:
                    if result_test is None:
                        result_test = "48"
                    elif result_test != "48":
                        result_test = 'Not valid'
                        break
                elif rule in test_data["5"]:
                    if result_test is None:
                        result_test = "5"
                    elif result_test != "5":
                        result_test = 'Not valid'
                        break
                elif rule in test_data["6"]:
                    if result_test is None:
                        result_test = "6"
                    elif result_test != "6":
                        result_test = 'Not valid'
                        break
                else:
                    if result_test is None:
                        result_test = "7"
                    elif result_test != "7":
                        result_test = 'Not valid'
                        break

            elif rule_ans[rule] == 'No':
                if rule in test_data["2"]:
                    if result_test is None:
                        result_test = "2"
                    elif result_test != "2":
                        result_test = 'Not valid'
                        break
                elif rule in test_data["3"]:
                    if result_test is None:
                        result_test = "3"
                    elif result_test != "3":
                        result_test = 'Not valid'
                        break
                elif rule in test_data["48"]:
                    if result_test is None:
                        result_test = "48"
                    elif result_test != "48":
                        result_test = 'Not valid'
                        break
                elif rule in test_data["5"]:
                    if result_test is None:
                        result_test = "5"
                    elif result_test != "5":
                        result_test = 'Not valid'
                        break
                elif rule in test_data["6"]:
                    if result_test is None:
                        result_test = "6"
                    elif result_test != "6":
                        result_test = 'Not valid'
                        break
                else:
                    if result_test is None:
                        result_test = "7"
                    elif result_test != "7":
                        result_test = 'Not valid'
                        break

        result_test = ans_text[result_test]
        return redirect(url_for('.answer', question="What experiment should I use?", answer=result_test))
    return render_template("test.html", test_rules=test_rules)

app.run(debug=True)
