#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 13:36:01 2023

@author: danger
"""

import time
import csv
from Puzzle_Class import Puzzle
from Random_puzzle import randomPuzzle

INSTRUCTIONS = {
    'main': '''
            Main Menu:
            Type 'upload' to store a puzzle.
            Type 'see' to view a stored puzzle.
            Type 'play' to try and solve an uploaded puzzle yourself.
            Type '!' to end the program or return to a previous menu.
            ''',
    'play': '''
            Here's what you can do:
            Type 'fill' to enter a value for a cell.
            Type 'hint' to have the computer fill a cell for you.
            Type 'solve' to view the solution and end the game.
            Type '!' to go back to the main menu.
            ''',
    'choice': '''
            Would you like to play a stored puzzle or a random puzzle?
            Type 'stored' to play a stored puzzle.
            Type 'random' to play a random puzzle.
            Type '!' to go back to the main menu.
            '''
}


def giveHint(puzzle, solution, finished):
    print("Enter a row and a column (separated by a space). ")
    (row, col) = list(map(int, input().split()))
    row = row - 1
    col = col - 1

    if puzzle.get_entry(row, col) != 0:
        print("That cell is already filled!")

    else:
        puzzle.set_entry(row, col, solution.get_entry(row, col))
        if len(puzzle.empties()) == 0:
            finished = True
            print("The puzzle is solved!")

    return puzzle, finished


def fillEntry(puzzle, solution, finished, mistakes):
    print("Enter a row, column, and value (separated by spaces). ")
    (row, col, val) = list(map(int, input().split()))
    row = row - 1
    col = col - 1

    if puzzle.get_entry(row, col) != 0:
        print("That cell is already filled!")

    else:
        if solution.get_entry(row, col) == val:
            print("Nice job!")
            puzzle.set_entry(row, col, val)
            if len(puzzle.empties()) == 0:
                finished = True
                print("The puzzle is solved!")
        else:
            mistakes += 1
            print("Not quite! Mistakes:", mistakes)

    return puzzle, finished, mistakes


def userSolves(puzzle, solution):  # output = num mistakes, num hints, finished
    mistakes = 0
    hints = 0
    finished = False

    print(INSTRUCTIONS['play'])
    next_move = input("Next move? ").lower()

    actions = ['fill', 'hint', 'solve', '!']
    while not finished:

        if next_move == '!':
            break

        else:
            if next_move not in actions:
                print("Input not understood.")
            elif next_move == 'fill':
                (puzzle, finished, mistakes) = fillEntry(puzzle, solution, finished, mistakes)
            elif next_move == 'hint':
                hints += 1
                (puzzle, finished) = giveHint(puzzle, solution, finished)
            elif next_move == 'solve':
                finished = True
                print("Here is the solved puzzle:")

            if not finished:
                print(puzzle)
                print(INSTRUCTIONS['play'])
                next_move = input("Next move? ").lower()

    return mistakes, hints, finished


def playPuzzle(puzzle):
    if len(puzzle.empties()) == 0:
        print("This puzzle is already solved")
        return

    print("Current puzzle:")
    print(puzzle)

    solution = puzzle.solve()
    start = time.time()
    (mistakes, hints, finished) = userSolves(puzzle, solution)
    end = time.time() - start
    minutes = int(end // 60)
    seconds = round(end % 60, 2)

    if finished:
        print(solution)
        print("Stats:")
        print("It took you", minutes, "minute(s) and", seconds, "second(s) to finish the game.")
        print("You made", mistakes, "mistake(s).")
        print("You asked for", hints, "hint(s).")
    else:
        return


def playChoice(bank):
    print(INSTRUCTIONS['choice'])
    choices = ['stored', 'random', '!']
    user_choice = input().lower()

    while user_choice not in choices:
        print("Input not understood.", INSTRUCTIONS['choice'])
        user_choice = input().lower()

    if user_choice == '!':
        return
    elif user_choice == 'stored':
        puzzle = chooseFromBank(bank)
        if puzzle is None:
            return
        playPuzzle(puzzle)
    elif user_choice == 'random':
        print("Loading...")
        playPuzzle(randomPuzzle())


def chooseFromBank(bank):
    if len(bank) == 0:
        print("There are no stored puzzles. Type 'upload' to store a puzzle.")
        return
    else:
        print("Here are the stored puzzles.")
        for name in bank:
            print('-', name)
        puzzle_name = input("Which would you like to choose? ")
        if puzzle_name == '!':
            return
        while puzzle_name not in bank:
            print("There is no puzzle with that name.")
            print("Here are the stored puzzles.")
            for name in bank:
                print('-', name)
            puzzle_name = input("Which would you like to choose? ")
            if puzzle_name == '!':
                return
        return bank[puzzle_name]


def seePuzzle(bank):
    from_bank = chooseFromBank(bank)

    if from_bank is None:
        return
    else:
        print("Here is the puzzle:")
        print(from_bank)


def uploadPuzzle(bank):
    print("Enter each row in a single line, separated by spaces.")
    print("Enter 0 if the cell is empty.")

    puzzle_values = []
    for row_num in range(9):
        print("Row", row_num + 1, end=': ')
        row = list(map(int, input().split()))
        puzzle_values.append(row)

    name = input("Enter a name for this puzzle: ")
    while name == '!':
        print("Cannot name a puzzle '!'. Try again.")
        name = input("Enter a name for this puzzle: ")

    with open(name, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(puzzle_values)
    new_puzzle = Puzzle(name)

    bank[name] = new_puzzle
    print("New puzzle stored! Here it is:")
    print(new_puzzle)


def mainMenu(bank):
    print(INSTRUCTIONS['main'])
    user_input = input().lower()

    actions = ['upload', 'see', 'play', '!']
    while user_input != '!':

        if user_input not in actions:
            print("Input not understood.")
        elif user_input == 'upload':
            uploadPuzzle(bank)
        elif user_input == 'see':
            seePuzzle(bank)
        else:  # user_input == 'play'
            playChoice(bank)

        print(INSTRUCTIONS['main'])
        user_input = input().lower()

    print("Good game.")
