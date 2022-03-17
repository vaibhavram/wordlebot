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
    if len(answers) == 1 or len(answers) == 2:
        return({answers[0]: 1})
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
    guess = function(valid_answers, all_guesses, info, no)
    return(guess)

def check_guess(guess, answer, info):
    output = ""
    for i in range(LENGTH):
        if guess[i] == answer[i]:
            output += "X"
            info[i] = set(guess[i])
        elif guess[i] in answer:
            output += "O"
            info[i].discard(guess[i])
            info[LENGTH].add(guess[i])
        else:
            output += "-"
            for x in info:
                x.discard(guess[i])
    return output == "X"*LENGTH

def run_game(answers, guesses, function):
    s = open("submission.txt", "x")
    score_sum = 0
    n = len(answers)
    for i in range(n):
        guess = ""
        no = 0
        info = [set(string.ascii_lowercase) for x in range(LENGTH)] +[set()]
        file_output = ""
        while guess != answers[i] and no < 10:
            guess = make_guess(answers, guesses, info, function, no)
            file_output += guess
            solved = check_guess(guess, answers[i], info)
            if solved:
                file_output += "\n"
            else:
                file_output += ","
            no += 1
        score_sum += no
        print(str(i) + "/" + str(n) + ": " + file_output[0:len(file_output)-1])
        s.write(file_output)
    s.close()
    return(score_sum / len(answers))

def main():
    g = open("accepted_words.txt", "r")
    guesses = [x.strip() for x in g.readlines()]
    g.close()

    a = open("possible_answers.txt", "r")
    answers = [x.strip() for x in a.readlines()]
    a.close()

    start = time.time()
    score = run_game(answers, guesses + answers, solution_set_minimizer_avg)
    print("Score: " + str(score))
    end = time.time()
    print("Completed in " + str(round(end - start, 3)) + "seconds")

def solution_set_minimizer_avg(valid_answers, all_guesses, info, no):
    if no == 0:
        return("salet")
    sol_set = build_sol_set(all_guesses, valid_answers, lambda x : sum(x) / len(x), 0)
    # sol_set = build_sol_set(all_guesses, valid_answers, lambda x : max(x), 0)
    return(min(sol_set, key=sol_set.get))

main()