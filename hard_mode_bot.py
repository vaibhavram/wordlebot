import random 
import string

LENGTH = 5

def is_valid_word(word, info):
	for i in range(LENGTH):
		if word[i] not in info[i]:
			return(False)
	for letter in info[LENGTH]:
		if letter not in word:
			return(False)
	return(True)

def valid_answers(answers, info):
	valid = []
	for answer in answers:
		if is_valid_word(answer, info):
			valid.append(answer)
	return(valid)

def build_freq(words, info):
	freq_table = {letter : 0 for letter in string.ascii_lowercase}
	freq_pos_table = [{letter : 0 for letter in string.ascii_lowercase} for x in range(LENGTH)]
	count = 0
	for word in words:
		count += 1
		letters = set()
		for i in range(LENGTH):
			letters.add(word[i])
			freq_pos_table[i][word[i]] += 1
		for letter in letters:
			freq_table[letter] += 1
	return(freq_table, freq_pos_table)

def best_guess(words, freq_table, freq_pos_table):
	n = len(words)
	best_word = ""
	best_score = 0
	for word in words:
		score = 0
		letters = set()
		for i in range(LENGTH):
			score += freq_pos_table[i][word[i]]
			letters.add(word[i])
		for letter in letters:
			score += freq_table[letter]
		if score > best_score: # creating a bias here
			best_word = word 
			best_score = score
	return(best_word)

def make_guess(answers, info, function = best_guess):
	valid = valid_answers(answers, info)
	print("There are " + str(len(valid)) + " possible answers.")
	if len(valid) <= 15:
		print("These include: " + str(valid))
	freq_table, freq_pos_table = build_freq(valid, info)
	guess = function(valid, freq_table, freq_pos_table)
	return(guess)

def check_guess(guess, answer, info):
	output = []
	for i in range(LENGTH):
		if guess[i] == answer[i]:
			output.append("X")
			# for x in info:
			# 	x.discard(guess[i])
			info[i] = set(guess[i])
		elif guess[i] in answer:
			output.append("O")
			info[i].discard(guess[i])
			info[LENGTH].add(guess[i])
		else:
			output.append("-")
			for x in info:
				x.discard(guess[i])
	# print(info)
	print(*output)

def get_random_answer(answers):
	return(random.choice(answers))

def run_game(answers):
	# answer = get_random_answer(answers)
	answer= "watch"
	print("------------------------------")
	print("GAME START")
	print("Answer: " + answer.upper())
	guess = ""
	no = 1
	info = [set(string.ascii_lowercase) for x in range(LENGTH)] +[set()]
	while guess != answer and no <= 6:
		guess = make_guess(answers, info)
		print("Guess " + str(no) + ": " + guess.upper())
		check_guess(guess, answer, info)
		no += 1
	print("Game over. Answer is " + answer.upper())
	print("------------------------------")

def main():
	a = open("possible_answers.txt", "r")
	answers = [x.strip() for x in a.readlines()]
	a.close()

	run_game(answers)

main()