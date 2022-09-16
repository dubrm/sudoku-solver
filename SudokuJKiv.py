import numpy as np
import kivy
kivy.require('1.9.1')


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window

Window.size = (700, 600)
"""App window Size"""

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



class SudokuApp(App):
    """Application"""
    def build(self):
        return SudokuWidget()

if __name__ == '__main__':
    app = SudokuApp()
    app.run()
    
