# from nltk.tokenize import sent_tokenize
# import nltk
# nltk.download('punkt')
# import flask
from flask.app import Flask
# Feedback link
feedback_link = "http://localhost:3000/Feedback"
Questions_link = "http://localhost:3000/Questions"


# ignore
def splitter(st):
    return st.split("\n    - ")[1:]

# sample intents


greet = """
    - hey
    - Hey
    - hello
    - Hello
    - hi
    - Hi
    - hello there
    - good morning
    - good evening
    - hey there
    - let's go
    - hey dude
    - goodmorning
    - goodevening
    - good afternoon"""

# nltk
# tokenized_text=sent_tokenize(greet)

greet = splitter(greet)

what_to_do = """
    - What is the task
    - I don't know what to do
    - I don't know what to start
    - I didn't understand
    - I don't understand
    - definition of the task
    - Definition of the Task
    - Definition of the task
    - Definition
    - definition
    - Understanding the Task
    - Understanding the task
    - understanding the task
    - understanding task
    - Understanding task
    - Understanding Task
    - Task
    - task"""

what_to_do = splitter(what_to_do)

what_task = """
    - What is the plan
    - Goals and Plan
    - Goals and plan
    - goals and plan
    - Goals 
    - goals 
    - Goal
    - goal
    - plan
    - Plan
    - Setting Goals and Plan
    - Setting
    - setting"""

what_task = splitter(what_task)

strategy = """
    - Strategy
    - strategy
    - strategies
    - Strategies
    - Question
    - question
    - Questions
    - questions
    - Studying Strategies
    - Studying strategies
    - studying strategies
    - studying
    - Studying
    - Learning Tactics
    - Learning tactics
    - learning tactics
    - Tactics
    - tactics
    - tactic
    - Tactic
    - Learning
    - learning"""

strategy = splitter(strategy)

number_chosen = """
    - 1
    - 2
    - 3
    - 4
    - one
    - One
    - two
    - Two
    - three
    - Three
    - four
    - Four"""

number_chosen = splitter(number_chosen)


end_plan = """
    - end
    - End
    - $"""

end_plan = splitter(end_plan)


affirm = """
    - yes
    - y
    - Y
    - YES
    - indeed
    - Indeed
    - of course
    - Of course
    - that sounds good
    - That sounds good
    - Sounds good
    - sounds good
    - Finished
    - finished
    - I'm finished
    - Done
    - done
    - ok
    - OK
    - Ok
    - Okay
    - okay
    - Alright
    - alright
    - All right
    - all right
    - Sure
    - sure
    - correct
    - Great
    - great
    - good
    - Good
    - agree
    - Agree
    - right
    - Right"""

affirm = splitter(affirm)

deny = """
    - no
    - n
    - N
    - NO
    - never
    - I don't think so
    - don't like that
    - no way
    - not really"""

deny = splitter(deny)

repeat = """
    - switch tactic
    - Switch tactic
    - Switch Tactic
    - switch
    - Switch
    - tactic
    - Tactic"""

repeat = splitter(repeat)

# To change start text, go into Frontend
# To change further modules, see below
# The following is a module


def starting_phase1(res, flag, inp, fun):
    if flag:
        res.append("Okay, are you ready to start working on the task?")
        return ("starting_phase1", res)

    flag = True

    if inp in affirm:
        res.append("Awesome.. Let’s get a main idea of the task.")
        res.append("I would suggest you have a quick look at two tabs (prior knowledge) and (questions) in the main menu.")
        return start_prior(res, flag, inp, "starting_phase1")
    else:
        res.append("No problem, just let me know when you're ready.")
        return starting_phase1(res, flag, inp, "starting_phase1")


def start_prior(res, flag, inp, fun):  # Do not change this
    if flag:
        res.append(" Let me know when you are done.")  # This is starting response of the module
        return ("start_prior", res)  # if you're copying this module to create a new module, remember to change return ("can_you_skim", res) to return ("your_module_name", res)
    flag = True
    # The following deals with what happens when user enters affirm -- yes, y, Y, YES, sure, okay
    if inp in affirm:
        return agree_answer_prior(res, flag, inp, "start_prior")

# ignore the following, don't copy it if you are creating new module
    if inp == "":
        return ("start_prior", res)

    # The following deals with what happens when user enters anything else except affirm
    else:
        res.append("Okay, take your time.")
        return start_prior(res, True, inp, "start_prior")


def agree_answer_prior(res, flag, inp, fun):
    if flag:
        res.append("Perfect. Now, I would like to learn if you already know something about this topic. Would you mind answering a few questions on the page in front of you?")
        return ("agree_answer_prior", res)

    flag = True

    if inp in deny:
        return finish_prior(res, flag, inp, "agree_answer_prior")
    else:
        res.append("Okay, take your time.")
        return agree_answer_prior(res, flag, inp, "agree_answer_prior")


def finish_prior(res, flag, inp, fun):
    if flag:
        res.append("Great. Please answer the questions and let me know when you're done.")
        return ("finish_prior", res)

    flag = True

    if inp in affirm:
        res.append("Awesome")
        return read_intro(res, flag, inp, "finish_prior")
    else:
        res.append("Okay, take your time.")
        return finish_prior(res, flag, inp, "finish_prior")


def read_intro(res, flag, inp, fun):
    if flag:
        res.append("Have you read the introduction of the task yet?")
        return ("read_intro", res)
        
    flag = True
    if inp in affirm:
        res.append("Great")
        return there_are_questions(res, flag, inp, "read_intro")
    else:
        res.append("Can you read the instructions, please? You can find it on this page")
        return read_intro(res, flag, inp, "read_intro")


def there_are_questions(res, flag, inp, fun):
    if flag:
        res.append("Now, there are questions that you are supposed to answer at the tab (Questions) {Questions_link}")
        res.append("Can you have a look at them, please? That will help you to catch the answers :)")
        return ("there_are_questions", res)
        
    flag = True
    if inp in affirm:
        res.append("Perfect. Maybe we can move on now.")
        return is_task_clear(res, flag, inp, "there_are_questions")
    else:
        res.append("Being familiar with task instructions helps you to do well in the task.")
        return there_are_questions(res, flag, inp, "there_are_questions")


def is_task_clear(res, flag, inp, fun):
    if flag:
        res.append("Is the goal of the task clear to you?")
        return ("is_task_clear", res)
    flag = True
    if inp in affirm:
        res.append("Great!")
        return put_plan(res, flag, inp, "is_task_clear")
    else:
        res.append("Well, I suggest you back again to the aim of the task to get the main idea.")
        return read_intro(res, flag, inp, "is_task_clear")


def put_plan(res, flag, inp, fun):
    if flag: 
        res.append("Do you already have some plan for this task?")
        return ("put_plan", res)
        
    flag = True
    if inp in affirm:
        res.append("Perfect!")
        return write_your_plan(res, flag, inp, "put_plan")
    else:
        res.append("Planning has been shown to help students stay organized and efficient during the task.")
        return put_plan(res, flag, inp, "put_plan")


def write_your_plan(res, flag, inp, fun):
    if flag:
        res.append("Can you write your plan in this chat window? (If you finish from your plan type 'end')")
        return ("write_your_plan", res)

    flag = True

    if inp in end_plan:
        res.append("Awesome")
        return did_you_finish_under(res, flag, inp, "write_your_plan")
    else:
        res.append("Great!. Go ahead.")
        return write_your_plan(res, flag, inp, "write_your_plan")


"""
def did_you_put_goals(res, flag, inp, fun):
    if flag: 
        res.append("Did you put your goal and sub-goals to achieve this task?")
        return ("did_you_put_goals", res)
    flag = True
    if inp in affirm:
        return did_you_finish_under(res, flag, inp, "did_you_put_goals")
    else:
        res.append("Planning has been shown to help students stay organized and efficient during the task.")
        return did_you_put_goals(res, flag, inp, "did_you_put_goals")
"""


def did_you_finish_under(res, flag, inp, fun):
    if flag: 
        res.append("Are you good with the task instructions and what you plan to do in this task?")
        return ("did_you_finish_under", res)
    flag = True
    if inp in affirm:
        return strategies_1(res, flag, inp, "did_you_finish_under")
    else:
        return put_plan(res, flag, inp, "did_you_finish_under")


def strategies_1(res, flag, inp, fun):
    if flag:
        res.append("Now you have the task in tab (Task) study it to answer the questions in tab (Questions), there are some learning tactics that may help you while studying the text and answering the questions.")
        res.append("For example, do you want to start by skimming over the title and subtitles?")
        return ("strategies_1", res)
    flag = True
    if inp in affirm:
        res.append("Great!")
        return finish_strategies_1(res, flag, inp, "strategies_1")
    else:
        res.append("Okay, let’s try with other tactics.")
        return strategies_2(res, flag, inp, "strategies1")


def finish_strategies_1(res, flag, inp, fun):
    if flag:
        res.append("please skim and let me know when you are done.")
        return ("finish_strategies_1", res)
    flag = True
    if inp in affirm:
        return strategies_2(res, flag, inp, "finish_strategies_1")
    else:
        res.append("Okay, take your time.")
        return finish_strategies_1(res, flag, inp, "finish_strategies_1")


def strategies_2(res, flag, inp, fun):
    if flag:
        res.append("The following tactics may help you to understand the information in the text better: 1. Highlight the main ideas. 2. Taking notes that will illustrate the topic. 3. Summarize the article. 4. Learning new material and incorporating it into an existing knowledge base. So, which one would you like to try?")
        return ("strategies_2", res)
    flag = True
    if inp in number_chosen:
        return repeat_strategies(res, flag, inp, "strategies_2")
    else:
        return strategies_2(res, flag, inp, "strategies_2")


def repeat_strategies(res, flag, inp, fun):
    if flag:
        res.append("Great. Please take your time to study the text using the selected tactic and let me know when you are done. If you would like to switch to different tactic, just type “switch tactic” in the chat window, and I can list the tactics for you again.")
        return ("repeat_strategies", res)
    flag = True
    if inp in repeat and affirm:
        return strategies_2(res, flag, inp, "repeat_strategies")
    else:
        # res.append("Great!. Seems you are finished from answering the questions.")
        return great_after(res, flag, inp, "repeat_strategies")


def great_after(res, flag, inp, fun):
    if flag:
        res.append("How is it going? did the tactics you did help you to answer all the questions?")
        return ("great_after", res)
    flag = True
    if inp in affirm:
        return is_there_something(res, flag, inp, "great_after")
    else:
        res.append("I see you are still not finished with the questions.")
        return strategies_2(res, flag, inp, "great_after")


def is_there_something(res, flag, inp, fun):
    if flag: 
        res.append("Is there something I can help you with?")
        return ("is_there_something", res)
    flag = True
    if inp in affirm:
        return what(res, flag, inp, fun)
    else:
        return end(res, flag, inp, fun)


def what(res, flag, inp, fun):
    if flag: 
        res.append("Please allow me to help.")
        res.append("Okay, let me know what you need help with: Understanding the Task, Setting Goals and Plan, OR Learning Tactics")
        return ("what", res)

    flag = True
    if inp in what_to_do:
        res.append("To understand the task, you want to make sure that the task requirements are clear to you (i.e., what should you do), and also you want to make sure that you are clear about what your accomplishment at the end of task needs to be (for example, to correctly answer the quiz items).")
        return read_intro(res, flag, inp, fun)
    if inp in what_task:
        res.append("By setting goals, a student sets milestone for the task. Importantly, a student can use their goals to track their progress in the task. Setting goals positively affects learning motivation and performance. A plan contains one or more goals. A student may decide to change goals and plans during the task.")
        return put_plan(res, flag, inp, fun)
    if inp in strategy:
        res.append("A learning tactic is a technique that a learner employs to achieve a certain goal (such as a memory assist or a method of taking notes)  to understand the concepts in a textbook chapter and how they relate to one another.")
        return did_you_finish_under(res, flag, inp, fun)
    else:
        return end(res, flag, inp, fun)


def end(res, flag, inp, fun):
    res.append(f"It’s been a pleasure meeting you. Before you go, please answer a few questions on this page {feedback_link} to let me know how your experience with me went today. Thank you :)")
    return ("end", res)
 

# Ignore the following
app = Flask("New")

from flask import request, jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route("/chat")
@cross_origin(supports_credentials=True)
def chat():
    inp = request.args["inp"]
    fun = request.args["fun"]
    out = eval(f"{fun}([], False, '{inp}', {fun})")
    fun, out = out
    print(fun)
    # out = "\n".join(out)
    print(out)
    return jsonify([fun, out])


app.run(debug=True)
