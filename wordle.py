import random 

def get_guess(no):
	x = input("Guess " + str(no) + ": ")
	return(x)

def check_guess(guess, answer, guesses):
	assert guess in guesses
	output = []
	for i in range(0, len(guess)):
		if guess[i] == answer[i]:
			output.append("X")
		elif guess[i] in answer:
			output.append("O")
		else:
			output.append("-")
	print(*output)

def get_human_answer():
	print("Answer word: ")
	return(input())

def get_random_answer(answers):
	return(random.choice(answers))

def run_game(answers, guesses):
	answer = get_random_answer(answers)
	# answer = get_human_answer()
	print("------------------------------")
	print("Game start")
	guess = ""
	no = 1
	while guess != answer and no <= 6:
		guess = get_guess(no)
		check_guess(guess, answer, guesses)
		no += 1
	print("Game over. Answer is " + answer.upper())
	print("------------------------------")

def main():
	g = open("accepted_words.txt", "r")
	guesses = [x.strip() for x in g.readlines()]
	g.close()

	a = open("possible_answers.txt", "r")
	answers = [x.strip() for x in a.readlines()]
	a.close()

	run_game(answers, guesses)

main()