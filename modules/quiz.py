import json
import urllib
import methods


def retrieve(user_id, category, quantity):
	url = "https://opentdb.com/api.php?amount="+ quantity +"&category=11"
	response = urllib.urlopen(url)
	jsonData = json.loads(response.read())
	results = jsonData["results"]
	responseCode = jsonData["response_code"]
	questions = []
	if ( responseCode == 0 ) :
		for data in results:

			difficulty = data["difficulty"]
			category = data["category"]
			question = data["question"]
			correct_answer = data["correct_answer"]
			incorrect_answers = data["incorrect_answers"]
			options = []
			options.append(correct_answer)
			options.extend(incorrect_answers)
			
			questions.append({ "question" : question, "options" : options, "correct_answer" : correct_answer }) 

	return questions