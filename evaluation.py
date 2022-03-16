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

def build_sol_set(candidates, answers, function):
    outcomes = {}
    if len(answers) == 1:
        return({answers[0]: 1})
    for candidate in candidates:
        # print(candidate)
        candidate_outcomes = {}
        for answer in answers:
            result = get_guess_result(candidate, answer)
            candidate_outcomes[result] = candidate_outcomes.get(result, 0) + 1
        outcomes[candidate] = function(candidate_outcomes.values())
    return(outcomes)

def make_guess(all_answers, all_guesses, info, function, no):
    valid_answers = get_valid_answers(all_answers, info)
    guess = function(valid_answers, all_answers, all_guesses, info, no)
    return(guess)

def check_guess(guess, answer, info):
    output = []
    for i in range(LENGTH):
        if guess[i] == answer[i]:
            output.append("X")
            info[i] = set(guess[i])
        elif guess[i] in answer:
            output.append("O")
            info[i].discard(guess[i])
            info[LENGTH].add(guess[i])
        else:
            output.append("-")
            for x in info:
                x.discard(guess[i])

def run_game(answers, guesses, function):
    score_sum = 0
    for i in range(len(answers)):
        if i % (len(answers) // 20) == 0:
            j = i // (len(answers) // 20)
            print("[" + "=" * j + " " * (20 - j) + "]",end = "\r")
        guess = ""
        no = 0
        info = [set(string.ascii_lowercase) for x in range(LENGTH)] +[set()]
        while guess != answers[i] and no < 10:
            guess = make_guess(answers, guesses, info, function, no)
            check_guess(guess, answers[i], info)
            no += 1
        score_sum += no
    return(score_sum / len(answers))

def main(functions):
    g = open("accepted_words.txt", "r")
    guesses = [x.strip() for x in g.readlines()]
    g.close()

    a = open("possible_answers.txt", "r")
    answers = [x.strip() for x in a.readlines()]
    a.close()

    for function_name in functions:
        start = time.time()
        print("-- " + function_name + " --")
        score = run_game(answers, guesses, functions[function_name])
        print("Score: " + str(score))
        end = time.time()
        print("Completed in " + str(round(end - start, 3)) + "seconds")

#################
### FUNCTIONS ###
#################

# best so far
def additive_frequency_solver_valid(valid_answers, all_answers, all_guesses, info, no):
    freq_table, freq_pos_table = build_freq(valid_answers, info)
    best_word = ""
    best_score = 0
    for word in valid_answers:
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

# changing multiplier
def additive_frequency_solver_1pt3(valid_answers, all_answers, all_guesses, info, no):
    freq_table, freq_pos_table = build_freq(valid_answers, info)
    best_word = ""
    best_score = 0
    for word in valid_answers:
        score = 0
        letters = set()
        for i in range(LENGTH):
            score += freq_pos_table[i][word[i]]
            letters.add(word[i])
        for letter in letters:
            score += 1.3 * freq_table[letter]
        if score > best_score:
            best_word = word 
            best_score = score
    return(best_word)

# changing multiplier
def additive_frequency_solver_1pt2(valid_answers, all_answers, all_guesses, info, no):
    freq_table, freq_pos_table = build_freq(valid_answers, info)
    best_word = ""
    best_score = 0
    for word in valid_answers:
        score = 0
        letters = set()
        for i in range(LENGTH):
            score += freq_pos_table[i][word[i]]
            letters.add(word[i])
        for letter in letters:
            score += 1.2 * freq_table[letter]
        if score > best_score:
            best_word = word 
            best_score = score
    return(best_word)

# changing multiplier
def additive_frequency_solver_1pt1(valid_answers, all_answers, all_guesses, info, no):
    freq_table, freq_pos_table = build_freq(valid_answers, info)
    best_word = ""
    best_score = 0
    for word in valid_answers:
        score = 0
        letters = set()
        for i in range(LENGTH):
            score += freq_pos_table[i][word[i]]
            letters.add(word[i])
        for letter in letters:
            score += 1.1 * freq_table[letter]
        if score > best_score:
            best_word = word 
            best_score = score
    return(best_word)

# not as good when you allow non-answer candidates
def additive_frequency_solver_all_guesses(valid_answers, all_answers, all_guesses, info, no):
    freq_table, freq_pos_table = build_freq(valid_answers, info)
    best_word = ""
    best_score = 0
    for word in all_guesses:
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

# 3.58488 with trace
# 3.61339 with salet
def solution_set_minimizer_avg(valid_answers, all_answers, all_guesses, info, no):
    if no == 0:
        return("salet")
    sol_set = build_sol_set(all_guesses, valid_answers, lambda x : sum(x) / len(x))
    return(min(sol_set, key=sol_set.get))

# 3.81382 with aesir
def solution_set_minimizer_minimax(valid_answers, all_answers, all_guesses, info, no):
    if no == 0:
        return("aesir")
    sol_set = build_sol_set(all_guesses, valid_answers, lambda x : max(x))
    return(min(sol_set, key=sol_set.get))

functions = {"additive_frequency_solver_valid": additive_frequency_solver_valid,
             "additive_frequency_solver_1pt1": additive_frequency_solver_1pt1 #,
             # "additive_frequency_solver_1pt2": additive_frequency_solver_1pt2,
             # "additive_frequency_solver_1pt3": additive_frequency_solver_1pt3
             # "solution_set_minimizer_avg": solution_set_minimizer_avg,
             # "solution_set_minimizer_minimax": solution_set_minimizer_minimax
             }

main(functions)