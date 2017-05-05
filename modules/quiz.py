import json
import urllib
import methods
import random
import HTMLParser
from Tkinter import *
import ttk

parser = HTMLParser.HTMLParser()
canvas = "";

def on_configure(event):
    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    canvas.configure(scrollregion=canvas.bbox('all'))

def on_mousescroll(event):
	# enable scrolling; defined speed
	canvas.yview_scroll( -1 * (event.delta), "units")

def quizUI(user_id, category, number):
    global canvas;

    window = Tk()
    window.resizable(width=False, height=False)

    # Creating a canvas to allow scrolling
    canvas = Canvas(window, width=520, height=600)
    canvas.pack(side=LEFT, padx=30)

    # Scrollbar
    scrollbar = Scrollbar(window, command=canvas.yview)
    scrollbar.pack(side=LEFT, fill='y')
    canvas.configure(yscrollcommand = scrollbar.set)
    canvas.bind('<Configure>', on_configure)
    canvas.bind_all('<MouseWheel>', on_mousescroll)

    frame = Frame(canvas, width=600, pady=40);
    frame.grid()
    canvas.create_window((0,0), window=frame, anchor='nw')

    # Retrieve the list of questions 
    questions = retrieve(user_id, category, number)
    answers = {}

    for i in range(0, len(questions)):
        options = questions[i]["options"]

        questionLabel = Label(frame, 
          wraplength=500,
          text= parser.unescape(questions[i]["question"]),
          justify = LEFT,
          padx = 10).pack(side="top", pady=20, anchor=W)

        answers[i] = IntVar();

        for j in range(0, len(options)):
            Radiobutton(frame, 
                        text=parser.unescape(options[j]),
                        padx = 10, 
                        variable=answers[i], 
                        value=j).pack(side="top", anchor=W)
        
    submitBtn = Button(frame, text ="Submit", command = lambda: completedQuiz(window, questions, answers)).pack(side="right")
        
    # Center Window
    methods.centerWindow(window);
    mainloop()

def retrieve(user_id, category, quantity):
    url = "https://opentdb.com/api.php?amount="+ str(quantity) +"&category=11"
    # Read JSON data from url
    response = urllib.urlopen(url)
    jsonData = json.loads(response.read())
    results = jsonData["results"]
    responseCode = jsonData["response_code"]

    questions = []
    if ( responseCode == 0 ) :
        for data in results:
            # Place them all in their respective variables
            difficulty, category, question, correct_answer, incorrect_answers = data["difficulty"], data["category"], data["question"], data["correct_answer"], data["incorrect_answers"]
            
            # Append the incorrect_answers list to our options list
            options = []
            options.extend(incorrect_answers)

            # Calculate a random index to place our correct_answer in the options list
            random_index = random.randrange(len(options)+1);
            options.insert(random_index, correct_answer)

            # Append it in the form of an object/dictionary to our questions list
            questions.append({ "question" : question, "options" : options, "correct_answer" : random_index })

        # Shuffle our questions
        random.shuffle(questions, random.random)
        
        return questions

def completedQuiz(window, questions, answers):
	window.destroy();
	calculateResults(questions, answers);

def calculateResults(questions, answers):
    correct = 0
    incorrect = []
   
    for i in range(0, len(questions)):
        correct_answer = questions[i]["correct_answer"]
        selected_answer = answers[i].get()

        if ( selected_answer == correct_answer ) :
            print "Correct!"
            correct += 1
        else: 
            incorrect.append(i)
            print "Incorrect!"
            

    # Calculate percentage based on the no. of corrects over the no. of questions
    percentage = float(correct) / float(len(questions)) * 100
    #return percentage #what if I delete this?


    window = Tk()
    window.resizable(width=False, height=False)
    window.title("Scoreboard")

    # Creating a canvas to allow scrolling
    canvas = Canvas(window, width=500, height=400)
    canvas.pack(side=LEFT, padx=30)

    frame = Frame(canvas, width=500, pady=40);
    frame.pack(expand=1)
    canvas.create_window((0,0), window=frame, anchor='nw')


    label = Label(frame, text= percentage, anchor="center")
    label.pack(fill="x", anchor="center")

    label.config(font=("Courier", 50))
     
    expgain = Label(frame, text = expadder(percentage))
    expgain.pack()
    expgain.config(font=("Courier",30))
    

    methods.centerWindow(window);
    window.mainloop()
    
def expadder(percentage):
	exp = 0 # replace this by getting the actual value from the user's json
	if percentage == 100:
	    exp += 100
	    return 100
	else:
	    if percentage <= 75:
	        exp += 50
	        return 50
	    else:
	        exp += 20
	        return 20    


