import json
import urllib
import methods
import random

answers = [];

def retrieve(user_id, category, quantity):
	url = "https://opentdb.com/api.php?amount="+ str(quantity) +"&category=11"
	response = urllib.urlopen(url)
	jsonData = json.loads(response.read())
	results = jsonData["results"]
	responseCode = jsonData["response_code"]
	questions = []
	if ( responseCode == 0 ) :
		for data in results:
			difficulty, category, question, correct_answer, incorrect_answers = data["difficulty"], data["category"], data["question"], data["correct_answer"], data["incorrect_answers"]
			options = []
			options.append(correct_answer)
			options.extend(incorrect_answers)
			questions.append({ "question" : question, "options" : options, "correct_answer" : correct_answer })
	
		random.shuffle(questions, random.random)

		# This is just needed to test the answers
		for data in questions :
			answers.append(random.choice(data["options"]))

		return questions

def calculateResults(questions):
	correct = 0;
	counter = 0;
	for data in questions:
		correct_answer = data["correct_answer"]
		selected_answer = answers[counter]
		if ( selected_answer == correct_answer ) :
			print "Correct!"
			correct += 1
		else: 
			print "Incorrect!"
		counter += 1

	percentage = float(correct) / float(counter) * 100
	return percentage
