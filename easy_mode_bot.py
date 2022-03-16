import random 
import string
import sys
import time

LENGTH = 5

def is_valid_word(word, info):
    for i in range(LENGTH):
        if word[i] not in info[i]:
            return(False)
    for letter in info[LENGTH]:
        if letter not in word:
            return(False)
    return(True)

def get_valid_answers(answers, info):
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

def get_guess_result(word, target):
    output = ""
    for i in range(LENGTH):
        if word[i] == target[i]:
            output += "X"
        elif word[i] in target:
            output += "O"
        else:
            output += "-"
    return(output)

def build_sol_set(candidates, answers, function, x_discount):
    outcomes = {}
    if len(answers) == 1:
        return({answers[0]: 1})
    elif len(answers) == 2:
        return({random.choice(answers): 1})
    for candidate in candidates:
        # print(candidate)
        candidate_outcomes = {}
        for answer in answers:
            result = get_guess_result(candidate, answer)
            candidate_outcomes[result] = candidate_outcomes.get(result, 0) + 1
        if "XXXXX" in candidate_outcomes.keys():
            candidate_outcomes["XXXXX"] = x_discount
        outcomes[candidate] = function(candidate_outcomes.values())
    return(outcomes)

def make_guess(all_answers, all_guesses, info, function, no):
    valid_answers = get_valid_answers(all_answers, info)
    print("There are " + str(len(valid_answers)) + " possible answers.")
    if len(valid_answers) <= 15:
        print("These include: " + str(valid_answers))
    guess = function(valid_answers, all_answers, all_guesses, info, no)
    return(guess)

def check_guess(guess, answer, info):
    output = []
    for i in range(LENGTH):
        if guess[i] == answer[i]:
            output.append("X")
            # for x in info:
            #   x.discard(guess[i])
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

def run_game(answers, guesses, function):
    # answer = get_random_answer(answers)
    answer= "round"
    print("------------------------------")
    print("GAME START")
    print("Answer: " + answer.upper())
    guess = ""
    no = 0
    info = [set(string.ascii_lowercase) for x in range(LENGTH)] +[set()]
    while guess != answer and no < 6:
        guess = make_guess(answers, guesses, info, function, no)
        print("Guess " + str(no + 1) + ": " + guess.upper())
        check_guess(guess, answer, info)
        no += 1
        # print(info)
    print("Game over. Answer is " + answer.upper())
    print("------------------------------")

def main():
    g = open("accepted_words.txt", "r")
    guesses = [x.strip() for x in g.readlines()]
    g.close()

    a = open("possible_answers.txt", "r")
    answers = [x.strip() for x in a.readlines()]
    a.close()

    run_game(answers, guesses, solution_set_minimizer_avg)

#################
### FUNCTIONS ###
#################

def solution_set_minimizer_avg(valid_answers, all_answers, all_guesses, info, no):
    if no == 0:
        return("salet")
    sol_set = build_sol_set(all_guesses, valid_answers, lambda x : sum(x) / len(x), 0)
    return(min(sol_set, key=sol_set.get))

main()