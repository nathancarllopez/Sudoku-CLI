'''
Random puzzle function
'''

import random
from Puzzle_Class import Puzzle

def solutionCollect(puzzle):
    solutions = []
    num_solutions = len(solutions)

    if len(puzzle.empties()) == 0:
        solutions.append(puzzle)

    else:
        guesses = puzzle.guessStack()
        num_guesses = len(guesses)

        while num_solutions < 2 and num_guesses > 0:
            next_puzzle = guesses.pop()
            empty_count = len(next_puzzle.empties())

            if empty_count == 0:
                solutions.append(next_puzzle)
            else:
                if not next_puzzle.contraCheck():
                    kids = next_puzzle.guessStack()
                    for kid in kids:
                        guesses.append(kid)

            num_solutions = len(solutions)
            num_guesses = len(guesses)

    return solutions


def hasUniqueSolution(puzzle):
    count = len(solutionCollect(puzzle))

    if count > 1:
        return False
    elif count == 1:
        return True
    elif count < 1:
        return


def randomPuzzle():
    '''

    Pseudocode:
    1) Start with a blank puzzle
    2) Choose a random entry and fill with a random value from the options at that entry
    3) Run hasUniqueSolution on the new puzzle
    4) Repeat steps 2 & 3 until hasUniqueSolution returns True

    '''

    random_puzzle = Puzzle('blank')
    empty_slots = [(row, col) for row in range(9) for col in range(9)]
    random_puzzle_options = random_puzzle.options()

    while True:
        (rand_row, rand_col) = empty_slots.pop(random.randrange(len(empty_slots)))
        rand_val = random.choice(random_puzzle_options[rand_row][rand_col])
        random_puzzle.set_entry(rand_row, rand_col, rand_val)

        if hasUniqueSolution(random_puzzle):
            # print("Done")
            return random_puzzle
        else:
            if hasUniqueSolution(random_puzzle) is None:
                # print("Not done", rand_row + 1, rand_col + 1, rand_val)
                random_puzzle.set_entry(rand_row, rand_col, 0)
                empty_slots.append((rand_row, rand_col))
                # print(random_puzzle)
            random_puzzle_options = random_puzzle.options()