from modules import user
from modules import quiz

questions = quiz.retrieve("11", "3")
quiz.calculateResults(questions);