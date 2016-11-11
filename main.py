# -*- coding: utf-8 -*-

import numpy as np
import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window

Window.size = (800, 600)


class SudokuSquare(TextInput):
    """A Sudoku Square can only contain one digit"""
    pass


class SudokuGrid(GridLayout):
    """9*9 input Grid."""

    def __init__(self, **kwargs):
        super(SudokuGrid, self).__init__(cols=3, spacing=[5, 5], **kwargs)
        self.squares = []
        for i in range(9):
            subgrid = GridLayout(cols=3)
            for j in range(9):
                square = SudokuSquare()
                subgrid.add_widget(square)
                self.squares.append(square)
            self.add_widget(subgrid)

    def to_array(self):
        user_input = [0 if square.text == '' else int(square.text)
                      for square in self.squares]
        subgrids = np.vsplit(np.array(user_input).reshape(27, 3), 9)
        grid = np.vstack((np.hstack(subgrids[0:3]),
                          np.hstack(subgrids[3:6]),
                          np.hstack(subgrids[6:9])))
        return grid

    def update_from_array(self, grid):
        subgrids = [np.hsplit(_, 3) for _ in np.vsplit(grid, 3)]
        output_values = np.vstack(subgrids).reshape(1, 81)[0]
        for square, value in zip(self.squares, output_values):
            square.text = str(value)


class SudokuWidget(Widget):
    """Main Widget of the Sudoku App"""
    grid_widget = ObjectProperty(None)

    def _solve(self):
        """Recursive solving method based on 2 methods:
                - First it finds squares only allowing 1 possibility and fills
                them
                - Then it bruteforces the remaining squares
        """
        just_one_more_turn = False  # Hahaha LOL
        finished = True  # by default, we assume there is no empty square
        brute_needed = {}
        print(self.grid)

        for r in range(9):  # row index
            for c in range(9):  # column index
                subgrid = self.grid[(3 * int(r / 3)):(3 * int(r / 3) + 3),
                                    (3 * int(c / 3)):(3 * int(c / 3) + 3)]
                if self.grid[r, c] == 0:
                    finished = False  # there is at least one empty square
                    possibilities = [digit for digit in range(1, 10)
                                     if (digit not in self.grid[r, :] and
                                         digit not in self.grid[:, c] and
                                         digit not in subgrid)]
                    if len(possibilities) == 1:
                        self.grid[r, c] = possibilities[0]
                        just_one_more_turn = True
                    elif (not brute_needed or
                          len(possibilities) <
                          len(brute_needed['possibilities'])):  # perfs
                        brute_needed['r'] = r
                        brute_needed['c'] = c
                        brute_needed['possibilities'] = possibilities

        if just_one_more_turn:
            return self._solve()  # − Luke, this is recursion. − Nooooooo....
        else:
            if finished:
                return finished  # Yeah!
            else:  # Here starts BruteforceLand
                print('BRUTEFORCE!!!')
                r = brute_needed['r']
                c = brute_needed['c']
                for possibility in brute_needed['possibilities']:
                    previous_grid = np.array(self.grid)
                    self.grid[r, c] = possibility
                    finished = self._solve()
                    if finished:
                        return finished
                    else:
                        self.grid = np.array(previous_grid)
                # if the loop ends, it means that the grid has no solution
                return False

    def solve(self):
        """Method called by the 'Solve it!' button."""
        self.grid = self.grid_widget.to_array()
        solved = self._solve()
        if solved:
            self.grid_widget.update_from_array(self.grid)
        else:
            print('Error')


class SudokuApp(App):
    """Application"""
    def build(self):
        return SudokuWidget()


if __name__ == '__main__':
    app = SudokuApp()
    app.run()
