#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 13:36:01 2023

@author: danger
"""

import csv
import copy

BOX_SIZE = 3 # Puzzle size is controlled here: puzzle size = box_size^2 x box_size^2
all_boxes = [] # The locations of all the cells in each box.
for i in range(BOX_SIZE):
    for j in range(BOX_SIZE):
        new_box = []
        for k in range(BOX_SIZE * i, BOX_SIZE * (i+1)):
            for l in range(BOX_SIZE * j, BOX_SIZE * (j+1)):
                new_box.append((k,l))
        all_boxes.append(new_box)

class Puzzle():
    def __init__(self, filename):
        '''
        A puzzle is stored as a collection of rows, implemented as a nested list

        Parameters
        ----------
        filename : CSV file
            Numeric values of each slot in the puzzle are stored here. Empty slots are stored as a zero

        Attributes
        -------
        self.values : (nested) list
            Numeric values are stored as a list of rows

        '''
        self.values = []
        with open(filename, 'r') as csvpuzzle:
            all_values = csv.reader(csvpuzzle, delimiter = ',')
            for row in all_values:
                print(row)
                row = list(map(int,row))
                self.values.append(row)
                
    def get_entry(self, row, column):
        return self.values[row][column]
    
    def set_entry(self, row, column, value):
        self.values[row][column] = value
                
    def cells(self, value):
        '''
        Returns a list of all cells filled with value
        '''
        cells_with_value = []
        for row in range(9):
            for col in range(9):
                if self.values[row][col] == value:
                    cells_with_value.append((row, col))
        return cells_with_value
                    
    def empties(self):
        '''
        Returns a list of all empty cells
        '''
        return self.cells(0)
    
    def options(self):
        '''
        Returns a nested dictionary of possibilities for each empty cell.
        The outer dictionary is keyed by the rows of the puzzle, with an inner dictioanry as a value
        The inner dictionaries are keyed by the columns of the puzzle, with a list of numeric values that each empty cell could have
        '''
        # Build an empty dictionary based on the empty cells
        options = {}
        for (row, col) in self.empties():
            if options.get(row) == None:
                options[row] = {col : []}
            else:
                options[row][col] = []
        # Fill dictionary
        values = [1,2,3,4,5,6,7,8,9]
        for val in values:
            val_cells = self.cells(val)
            bad_empties = []
            for (val_row, val_col) in val_cells:
                # Search through val_row
                for col in range(9):
                    if self.values[val_row][col] == 0:
                        bad_empties.append((val_row, col))
                # Search through val_col
                for row in range(9):
                    if self.values[row][val_col] == 0:
                        if (row, val_col) not in bad_empties:
                            bad_empties.append((row, val_col))
                # Search through the box containing (val_row, val_col)
                for box in all_boxes:
                    exist_count = box.count((val_row, val_col))
                    if exist_count > 0:
                        val_box = box
                for (row, col) in val_box:
                    if self.values[row][col] == 0:
                        if (row, col) not in bad_empties:
                            bad_empties.append((row, col))
            for (row, col) in self.empties():
                if (row, col) not in bad_empties:
                    options[row][col].append(val)
        return options
    
    def svcells(self):
        '''
        An empty cell is called 'single-valued' if there is only one numeric value it could take
        '''
        # Create the options for self
        options = self.options()
        # Search options for cells with only one value
        sv_cells = []
        for row in options:
            for (col, val) in options[row].items():
                if len(val) == 1:
                    sv_cells.append((row, col, val[0]))
        return sv_cells
    
    def lvcells(self, value):
        '''
        An empty cell is called 'lonely-valued' if it is the only cell in a row/column/box that can take on a particular value
        '''
        # Create the options for self and an empty list to store the lonely cells
        options = self.options()
        lv_cells = []
        # Find the lonely value cells in the rows
        for row in options:
            row_cells = []
            for (col, vals) in options[row].items():
                if vals.count(value) != 0:
                    row_cells.append((row, col))
            if len(row_cells) == 1:
                lv_cells.append(row_cells[0])
        # Find the lonely value cells in the columns
        for position in range(9):
            col_cells = []
            for (row, col_options) in options.items():
                if col_options.get(position) != None:
                    if col_options[position].count(value) !=0:
                        col_cells.append((row, position))
            if len(col_cells) == 1:
                if col_cells[0] not in lv_cells:
                    lv_cells.append(col_cells[0])
        # Find the lonely value cells in the boxes
        for box in all_boxes:
            box_cells = []
            for (row, col) in box:
                if options.get(row) != None:
                    if options[row].get(col) != None:
                        if options[row][col].count(value) != 0:
                            box_cells.append((row, col))
            if len(box_cells) == 1:
                if box_cells[0] not in lv_cells:
                    lv_cells.append(box_cells[0])
        return lv_cells
    
    def easyFill(self):
        '''
        Fills all single value and lonely value cells:
        First, looks and fills all single value cells, updating after each fill, until none remain
        Second, checks if there are any empty cells left, returns the solved puzzle if not
        Third, if empty cells remain, finds and fills lonely value cells, updating after each fill to check for single value cells
        Returns a puzzle with all single value and lonely value cells filled
        '''
        # Find and fill single value cells
        sv_cells = self.svcells()
        while len(sv_cells) > 0:
            (row, col, val) = sv_cells[0]
            self.values[row][col] = val
            sv_cells = self.svcells()
        # If no empty cells remain, return the puzzle
        if len(self.empties()) == 0:
            return self
        # Otherwise, find and fill lonely value cells
        else:
            values = [1,2,3,4,5,6,7,8,9]
            index = 0
            while index < len(values):
                val = values[index]
                lv_cells = self.lvcells(val)
                if len(lv_cells) > 0:
                    for (row, col) in lv_cells:
                        self.values[row][col] = val
                    sv_cells = self.svcells()
                    while len(sv_cells) > 0:
                        (row, col, val) = sv_cells[0]
                        self.values[row][col] = val
                        sv_cells = self.svcells()
                    index = 0
                else:
                    index += 1
            return self
        
    def contraCheck(self):
        '''
        We check a puzzle for a contradiction after applying easyFill
        A puzzle has a contradiction if there is an empty cell with no available options
        '''
        # Create the options for self
        options = self.options()
        contradiction = False
        # Look through options for a contradiction
        for (row, col) in self.empties():
            if options[row][col] == []:
                contradiction = True
        return contradiction
    
    def guessStack(self):
        '''
        Returns a stack of possible puzzles by guessing a value for an empty cell
        After a value is guessed, easyFill is run on the result, and the output is stored in the stack
        '''
        # Create the options for self
        options = self.options()
        # Find the first cell with the smallest number of options
        guess = ()
        guess_count = 10
        for row in options:
            for (col, val) in options[row].items():
                if len(val) < guess_count:
                    guess = (row, col, val)
                    guess_count = len(val)
        # Relabel for clarity
        g_row = guess[0]
        g_col = guess[1]
        g_vals = guess[2]
        # Create a stack of guess_puzzles
        guess_stack = []
        for val in g_vals:
            duplicate = copy.deepcopy(self)
            duplicate.values[g_row][g_col] = val
            duplicate.easyFill()
            guess_stack.append(duplicate)
        return guess_stack
    
    def solve(self):
        '''
        Main solving function. Works via backtracking
        First, checks for empty cells, returns puzzle if there are none.
        Second, if there are empty cells, runs guessStack on the input puzzle to create a main stack
        Third, pulls the top puzzle off the stack and checks if it has empty cells, returns top puzzle if not
        Fourth, if top puzzle has empty cells, guessStack is run on the top puzzle and the new puzzles are added to the top of the main stack
        These last two steps are repeated until a solved puzzle is found
        '''
        empty_count = len(self.empties())
        if empty_count == 0:
            return self
        else:
            stack = self.guessStack()
            while empty_count > 0:
                puzzle = stack.pop()
                empty_count = len(puzzle.empties())
                if empty_count == 0:
                    return puzzle
                else:
                    if not puzzle.contraCheck():
                        kids = puzzle.guessStack()
                        for kid in kids:
                            stack.append(kid)
                            
    def __str__(self):
        '''
        Prints (an ugly but readable version of) the puzzle
        '''
        count = 0
        print('-' * 43)
        for row in self.values:
            count += 1
            if count % 4 == 0:
                print('-' * 43)
                count = 1
            print('|', end = '')
            for j in range(3):
                for k in range(3):
                    if row[k + 3 * j] != 0:
                        print(' ', row[k + 3 * j], end = ' ')
                    else:
                        print(' ', '_', end = ' ')
                print(' |', end = '')
            print()
            print()
        print('-' * 43)
        return ''












