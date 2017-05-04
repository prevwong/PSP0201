import json
import urllib
import methods
import random
import HTMLParser
from Tkinter import *
import ttk

parser = HTMLParser.HTMLParser()
canvas = "";
answers = {}

def on_configure(event):
    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    canvas.configure(scrollregion=canvas.bbox('all'))

def on_mousescroll(event):
	# enable scrolling; defined speed
	canvas.yview_scroll( -1 * (event.delta), "units")

def quizUI():
	global canvas, answers;

	root = Tk()
	root.resizable(width=False, height=False)

	# Creating a canvas to allow scrolling
	canvas = Canvas(root, width=550, height=600)
	canvas.pack(side=LEFT, padx=30)

	# Scrollbar
	scrollbar = Scrollbar(root, command=canvas.yview)
	scrollbar.pack(side=LEFT, fill='y')
	canvas.configure(yscrollcommand = scrollbar.set)
	canvas.bind('<Configure>', on_configure)
	canvas.bind_all('<MouseWheel>', on_mousescroll)

	frame = Frame(canvas, width=600, pady=40);
	frame.grid()
	canvas.create_window((0,0), window=frame, anchor='nw')

	# Retrieve the list of questions 
	questions = retrieve("11", "9", "10")


	for i in range(0, len(questions)):
		options = questions[i]["options"]

		questionLabel = Label(frame, 
		  wraplength=500,
  		  text= parser.unescape(questions[i]["question"]),
	      justify = LEFT,
	      padx = 10).pack(side="top", pady=20, anchor=W)

		answers[i] = IntVar(master=root);
		answers[i].set(0);
		
		for j in range(0, len(options)):
			Radiobutton(frame, 
		                text=parser.unescape(options[j]),
		                padx = 10, 
		                variable=answers[i], 
		                value=j).pack(side="top", anchor=W)
		
	submitBtn = Button(frame, text ="Submit", command = lambda: calculateResults(questions)).pack(side="right")

	# Center Window
	methods.centerWindow(root);
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

def calculateResults(questions):
	correct = 0;
	for i in range(0, len(questions)):
		correct_answer = questions[i]["correct_answer"]
		selected_answer = answers[i].get()

		if ( selected_answer == correct_answer ) :
			print "Correct!"
			correct += 1
		else: 
			print "Incorrect!"

	# Calculate percentage based on the no. of corrects over the no. of questions
	percentage = float(correct) / float(len(questions)) * 100
	print percentage

quizUI();
